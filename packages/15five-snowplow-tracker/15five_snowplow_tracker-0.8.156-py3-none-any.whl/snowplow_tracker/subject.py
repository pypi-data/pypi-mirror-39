"""
    subject.py

    Copyright (c) 2013-2014 Snowplow Analytics Ltd. All rights reserved.

    This program is licensed to you under the Apache License Version 2.0,
    and you may not use this file except in compliance with the Apache License
    Version 2.0. You may obtain a copy of the Apache License Version 2.0 at
    http://www.apache.org/licenses/LICENSE-2.0.

    Unless required by applicable law or agreed to in writing,
    software distributed under the Apache License Version 2.0 is distributed on
    an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
    express or implied. See the Apache License Version 2.0 for the specific
    language governing permissions and limitations there under.

    Authors: Anuj More, Alex Dean, Fred Blundun
    Copyright: Copyright (c) 2013-2014 Snowplow Analytics Ltd
    License: Apache License Version 2.0

    !!!MODIFIED BY 15FIVE!!! 
    Modifiers: Andrii Pleskach, Paul Logston

"""

from contracts import contract, new_contract

SUPPORTED_PLATFORMS = set(["pc", "tv", "mob", "cnsl", "iot", "web", "srv", "app"])
DEFAULT_PLATFORM = "pc"

new_contract("subject", lambda x: isinstance(x, Subject))

new_contract("supported_platform", lambda x: x in SUPPORTED_PLATFORMS)


class Subject(object):
    """
        Class for an event subject, where we view events as of the form

        (Subject) -> (Verb) -> (Object)
    """
    def __init__(self):

        self.standard_nv_pairs = {"p": DEFAULT_PLATFORM}

    @contract
    def set_platform(self, value):
        """
            :param  value:          One of ["pc", "tv", "mob", "cnsl", "iot", "web", "srv", "app"]
            :type   value:          supported_platform
            :rtype:                 subject
        """
        self.standard_nv_pairs["p"] = value
        return self

    @contract
    def set_user_id(self, user_id):
        """
            :param  user_id:        User ID
            :type   user_id:        string
            :rtype:                 subject
        """
        self.standard_nv_pairs["uid"] = user_id
        return self

    @contract
    def set_screen_resolution(self, width, height):
        """
            :param  width:          Width of the screen
            :param  height:         Height of the screen
            :type   width:          int,>0
            :type   height:         int,>0
            :rtype:                 subject
        """
        self.standard_nv_pairs["res"] = "".join([str(width), "x", str(height)])
        return self

    @contract
    def set_viewport(self, width, height):
        """
            :param  width:          Width of the viewport
            :param  height:         Height of the viewport
            :type   width:          int,>0
            :type   height:         int,>0
            :rtype:                 subject
        """
        self.standard_nv_pairs["vp"] = "".join([str(width), "x", str(height)])
        return self

    @contract
    def set_color_depth(self, depth):
        """
            :param  depth:          Depth of the color on the screen
            :type   depth:          int
            :rtype:                 subject
        """
        self.standard_nv_pairs["cd"] = depth
        return self

    @contract
    def set_timezone(self, timezone):
        """
            :param  timezone:       Timezone as a string
            :type   timezone:       string
            :rtype:                 subject
        """
        self.standard_nv_pairs["tz"] = timezone
        return self

    @contract
    def set_lang(self, lang):
        """
            Set language.

            :param  lang:           Language the application is set to
            :type   lang:           string
            :rtype:                 subject
        """
        self.standard_nv_pairs["lang"] = lang
        return self

    @contract
    def set_domain_user_id(self, duid):
        """
            Set the domain user ID

            :param duid:            Domain user ID
            :type  duid:            string
            :rtype:                 subject
        """
        self.standard_nv_pairs["duid"] = duid
        return self

    @contract
    def set_ip_address(self, ip):
        """
            Set the domain user ID

            :param ip:              IP address
            :type  ip:              string
            :rtype:                 subject
        """
        self.standard_nv_pairs["ip"] = ip
        return self

    @contract
    def set_useragent(self, ua):
        """
            Set the user agent

            :param ua:              User agent
            :type  ua:              string
            :rtype:                 subject
        """
        self.standard_nv_pairs["ua"] = ua
        return self

    @contract
    def set_network_user_id(self, nuid):
        """
            Set the network user ID field
            This overwrites the nuid field set by the collector

            :param nuid:            Network user ID
            :type  nuid:            string
            :rtype:                 subject
        """
        self.standard_nv_pairs["tnuid"] = nuid
        return self

    def set_custom(self, field, value):
        """
            Set custom field

            :param field:           Field name
            :param value:           Value for a field
        """
        self.standard_nv_pairs[field] = value
        return self

    def set_custom_by_name(self, field, value):
        """
            Set custom field by getting field name from SNOWPLOW_REVERTED_TRANSFORM_MAP

            :param field:           Field name
            :param value:           Value for a field
        """
        self.standard_nv_pairs[SNOWPLOW_REVERTED_TRANSFORM_MAP.get(field, field)] = value
        return self


SNOWPLOW_REVERTED_TRANSFORM_MAP = {
    "event": "e",
    "user_ipaddress": "ip",
    "app_id": "aid",
    "platform": "p",
    "txn_id": "tid",
    "user_id": "uid",
    "domain_userid": "duid",
    "network_userid": "nuid",
    "useragent": "ua",
    "user_fingerprint": "fp",
    "domain_sessionidx": "vid",
    "domain_sessionid": "sid",
    "dvce_created_tstamp": "dtm",
    "true_tstamp": "ttm",
    "dvce_sent_tstamp": "stm",
    "name_tracker": "tna",
    "v_tracker": "tv",
    "v_collector": "cv",
    "br_lang": "lang",
    "br_features_pdf": "f_pdf",
    "br_features_flash": "f_fla",
    "br_features_java": "f_java",
    "br_features_director": "f_dir",
    "br_features_quicktime": "f_qt",
    "br_features_realplayer": "f_realp",
    "br_features_windowsmedia": "f_wma",
    "br_features_gears": "f_gears",
    "br_features_silverlight": "f_ag",
    "br_cookies": "cookie",
    "br_colordepth": "cd",
    "os_timezone": "tz",
    "page_referrer": "refr",
    "page_url": "url",
    "page_title": "page",
    "doc_charset": "cs",
    "event_id": "eid",
    "contexts": "cx",
    "se_category": "se_ca",
    "se_action": "se_ac",
    "se_label": "se_la",
    "se_property": "se_pr",
    "se_value": "se_va",
    "unstruct_event": "ue_pr",
    "tr_orderid": "tr_id",
    "tr_affiliation": "tr_af",
    "tr_total": "tr_tt",
    "tr_tax": "tr_tx",
    "tr_shipping": "tr_sh",
    "tr_city": "tr_ci",
    "tr_state": "tr_st",
    "tr_country": "tr_co",
    "ti_orderid": "ti_id",
    "ti_sku": "ti_sk",
    "ti_name": "ti_nm",
    "ti_category": "ti_ca",
    "ti_price": "ti_pr",
    "ti_quantity": "ti_qu",
    "pp_xoffset_min": "pp_mix",
    "pp_xoffset_max": "pp_max",
    "pp_yoffset_min": "pp_miy",
    "pp_yoffset_max": "pp_may",
    "tr_currency": "tr_cu",
    "ti_currency": "ti_cu",
}
