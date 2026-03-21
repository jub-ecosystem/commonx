

from typing import Optional

class Helpers:
    @staticmethod
    def sanitize_null_id_none(v:Optional[str])->Optional[str]:
        """
        Docstring for sanitize_null_id_none
        
        :param v: Description
        :type v: Optional[str]
        :return: Description
        :rtype: str | None
        """ 
        if v is None:
            return v
        if not isinstance(v,str):
            raise ValueError("parent_id must be a string or None")
        null_values = {"", "null", "none", "undefined", "nil"}
        v_sanitized = v.strip()
        if v_sanitized.lower() in null_values:
            return None
        return v_sanitized
