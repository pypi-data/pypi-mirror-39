from __future__ import absolute_import

from collections import OrderedDict

from requests import session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from workfront.exceptions import WFException, raise_if_not_ok
import datetime as dt
from urllib import urlencode as urlencode


class WFEventType:
    CREATE = "CREATE"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
    SHARE = "SHARE"


class Workfront(object):
    '''
    @summary: A workfront service object that is used to interact with the
    Workfront API.

    Config
    ======
    Having a Workfront service object like :

    from workfront.workfront import Workfront
    wf = wf = Workfront('myuser@email.com', 'mysecret', 'my.workfront.com')

    Some parameters can be configured:

    * wf.refresh_session_time : Time in minutes after the session is recycled.
    After the given time, and before making another call, the WF service object
    will automatically re-login. Default is 25 minutes.

    * wf.on_retry_status : List of status on which the WF service object will
    retry a call before returnig the error response.
    Default value : [500, 401]

    * wf.relogin_retries : (integer) number of times that the WF service object
    will try to excecute a call after it was failed with an unauthorized(401)
    error. After every fail, it will try to re-login before trying again.
    Default value is 2

    NOTE: There are 2 types of retries:

    * relogin retries : when it returns 401, the object will re-login and call
    the endpoint again (with new credentials).
    This type of retry is affected by *relogin_retries* parameter.

    * urllib retries : when requests urllib internally retries after a failure
    call. This retry has a backoff policy and it will try 3 times.
    This type of retry is affected by *on_retry_status* parameter.
    '''
    def_wf_domain = "thebridgecorp.my.workfront.com"

    ON_RETRY_STATUS = [500, 401]

    RELOGIN_RETRIES = 2

    def __init__(self, user, passw, wf_domain=def_wf_domain):
        '''
        @param user: user used to login into WF (probably email)
        @param passw: password for the given user
        @param wf_domain: domain of the workfront instance. Probably something
        like corporation.my.workfront.com
        '''
        self.refresh_session_time = 25  # in minutes
        self.sess = None
        self.user = user
        self.passw = passw
        self._wf_last_connect = dt.datetime.now() - dt.timedelta(weeks=65)
        self.sess_id = None
        self.url_base = "https://{}/attask/api/v7.0/".format(wf_domain)
        self.on_retry_status = self.ON_RETRY_STATUS
        self.relogin_retries = self.RELOGIN_RETRIES

    def __create_session(self, retries=3):
        '''
        @return return a tunned request session object with some specific retry
         capabilities
        '''
        ss = session()
        retry = Retry(total=retries, read=retries, connect=retries,
                      backoff_factor=0.2,
                      status_forcelist=self.on_retry_status)
        adapter = HTTPAdapter(max_retries=retry)
        ss.mount('https://', adapter)
        return ss

    def get_api_url(self):
        return self.url_base

    @property
    def sess(self):
        # Force the service to reconnect after refresh_session_time to avoid
        # expired sessions
        tdiff = dt.datetime.now() - self._wf_last_connect
        if tdiff > dt.timedelta(minutes=self.refresh_session_time) or\
                self._sess is None:
            self.login()
        return self._sess

    @sess.setter
    def sess(self, value):
        self._sess = value

    def login(self):
        '''
        @summary: login against the WF API and save the session for future
        requests. If there is an active session, logout from it before login in
        again.
        '''
        if self._sess is not None:
            self.__logout(self._sess)

        ss = self.__create_session()
        url = self.url_base + "login?username=%s&password=%s"
        r = ss.post(url % (self.user, self.passw))
        if r.status_code is not 200:
            e = "Could not log in to Workfront: {}".format(r.json())
            raise WFException(e)
        self.sess_id = r.json()["data"]["sessionID"]
        self._wf_last_connect = dt.datetime.now()
        ss.headers.update({"SessionID": self.sess_id})
        self.sess = ss

    def __logout(self, ss):
        '''
        @summary: Log out from workfront, calling the logout endpoint
        @param ss: requests session object
        '''
        u = self.url_base + "logout"
        try:
            ss.get(u)
        except Exception:
            pass
        self.sess = None
        self.sess_id = None

    def logout(self):
        '''
        @summary: logout, invalidating the current session id
        '''
        self.__logout(self.sess)

    def __should_retry(self, req, relogin_retry):
        '''
        @return: True if the request should be retried.
        @note: This method calls to login, to re-login when it returns True.
        @param req: request object that has been made
        @param relogin_retry: amount of times that should retry. Or None.
        '''
        if req.status_code == 401:
            if relogin_retry is None:
                relogin_retry = self.relogin_retries
            if relogin_retry > 0:
                self.login()
                return True
        return False

    def _post(self, url, js, relogin_retry=None):
        '''
        @param url: url part of the object being posted (not the url base)
        @param js: json body to be send
        '''
        u = self.url_base + url
        r = self.sess.post(u, json=js)

        if self.__should_retry(r, relogin_retry):
            return self._post(url, js, relogin_retry=relogin_retry - 1)

        return r

    def _put(self, url, js=None, relogin_retry=None):
        '''
        @param url: url part of the object being put (not the url base)
        @param js: dictionary to be send as json body.
        '''
        u = self.url_base + url
        if js is not None:
            r = self.sess.put(u, json=js)
        else:
            r = self.sess.put(u)

        if self.__should_retry(r, relogin_retry):
            return self._put(url, js, relogin_retry=relogin_retry - 1)

        return r

    def _get(self, url, relogin_retry=None):
        '''
        @param url: url part of the object being get (not the url base)
        '''
        u = self.url_base + url
        r = self.sess.get(u)

        if self.__should_retry(r, relogin_retry):
            return self._get(url, relogin_retry=relogin_retry - 1)

        return r

    def _delete(self, url, relogin_retry=None):
        '''
        @param url: url part of the object being put (not the url base)
        '''
        u = self.url_base + url
        r = self.sess.delete(u)

        if self.__should_retry(r, relogin_retry):
            return self._delete(url, relogin_retry=relogin_retry - 1)

        return r

    def search_objects(self, obj, param_dict, fields=[], order_by=None,
                       from_index=None, limit=None):
        """
        @summary: Do a search of the objects restricted by the fields given in
        the param_dict

        @param obj: object code being searched
        @param param_dict: dictionary of query strings (key = value)
        @param fields: fields being retrieved for the object

        @type  order_by: OrderedDict
        @param order_by: Order by parameters. The order insertion determines
        the order by priority.
        (default: {"entryDate":"desc"})
            Ex: order = OrderedDict()
                order["name"] = "asc"
                order["entryDate"] = "desc"
                the order priority will be: by name asc and then entryDate desc

        @type from_index: int
        @param from_index: specify the first result index that should be
         returned (start at 0)

        @type limit: int
        @param limit: specify the maximum amount results that should be
        returned

        @rtype: dict
        @return: A dictionary with WF Projects
        """

        parameters = param_dict.copy()

        if from_index is not None and limit is not None:
            parameters.update({"$$FIRST": from_index, "$$LIMIT": limit})

        if isinstance(order_by, OrderedDict):
            index = 0
            for key, value in order_by.iteritems():
                index += 1
                parameters[key + "_" + str(index) + "_Sort"] = value

        url = "%s/search" % obj

        if len(parameters) > 0:
            # TODO: bug if a parameter contains "&"
            qs = ["{}={}".format(k, v) for k, v in parameters.items()]

            if len(fields) > 0:
                # TODO: bug if a parameter contains "&"
                qs.append("fields={}".format(",".join(fields)))

            qs = "&".join(qs)
            url = url + "?" + qs

        return self._get(url)

    def count_objects(self, obj, filters):
        """
        @summary: Do a count of the objects restricted by the fields given in
        the filters dictionary
        @param obj: object code being searched
        @param filters: dictionary of filter for query
        """

        url = "%s/count" % obj
        if len(filters) > 0:
            qs = urlencode(filters.items())
            url = url + "?" + qs

        return self._get(url)

    def get_object(self, obj, idd, fields=[]):
        '''
        @param obj: object code being retrieved
        @param idd: WF id of the object
        @param fields: list of fields being retrieved for the given object. If
        not given, the fields retrieved will be the custom one.
        '''
        url = "%s/%s" % (obj, idd)
        if len(fields):
            url = url + "?fields=%s" % ",".join(fields)
        return self._get(url)

    def put_object(self, obj, idd, param_dict={}):
        '''
        @summary: Do a put object
        @param obj: obj code
        @param idd: WF id of the object being put
        @param param_dict: dictionary of query strings (key = value)
        '''
        url = "%s/%s" % (obj, idd)
        qs = urlencode(param_dict.items())
        url = url + "?" + qs
        return self._put(url)

    def post_object(self, obj, param_dict={}):
        '''
        @summary: Do a post object
        @param obj: obj code
        @param param_dict: dictionary of query strings (key = value)
        '''
        r = self._post(obj, param_dict)
        raise_if_not_ok(r, obj)
        return r

    def action(self, obj, idd, action, param_dict):
        '''
        @summary: Perform an action for the object given.
        @param obj: obj code
        @param idd: WF id of the object being put
        @param action: action being done for the given object
        @param param_dict: dictionary of query strings (key = value)
        '''
        param_dict["action"] = action
        return self.put_object(obj, idd, param_dict)

    def bulk_action(self, obj, action, param_dict):
        '''
        @summary: Perform an action for the object given.
        @param obj: obj code
        @param action: action being done for the given type of object
        @param param_dict: json with fields required by the action
        '''
        url = "{}?action={}".format(obj, action)
        return self._put(url, js=param_dict)

    def get_api_key(self):
        '''
        @summary: Get a Workfront API key.
        '''
        u = self.url_base + "USER?action=getApiKey&username=%s&password=%s"
        u = u % (self.user, self.passw)
        return self.sess.put(u).json()["data"]["result"]

    def gen_api_key(self):
        '''
        @summary: Generate a Workfront API key.
        '''
        u = self.url_base + "USER/generateApiKey?username=%s&password=%s"
        u = u % (self.user, self.passw)
        return self.sess.put(u).json()["data"]["result"]
