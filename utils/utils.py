"""
This file contains the classes and functions that is used throughout the project.
"""

import streamlit as st


class SessionState:
    """
    Class for managing session state in Streamlit applications.
    """

    def __init__(self, key: str, default_state: bool = False):
        """
        Initializes a new instance of the SessionState class.

        Parameters:
            key (str): The key to identify the session state.
            default_state (bool): The default state value if the key is not found in the session
            state.

        Returns:
            None
        """
        self.key = key
        self.default_state = default_state

        if self.key not in st.session_state:
            st.session_state[self.key] = self.default_state

    def sessionstate_true(self) -> None:
        """
        Sets the value of the specified key in the session state to True.

        Returns:
            None
        """
        st.session_state[self.key] = True

    def sessionstate_false(self) -> None:
        """
        Sets the value of the specified key in the session state to False.

        Returns:
            None
        """
        st.session_state[self.key] = False

    def check_sessionstate(self) -> bool:
        """
        Returns the value of the specified key in the session state.

        Returns:
            bool: The value of the specified key in the session state.
        """
        return st.session_state[self.key]

    def write_currentstate(self) -> None:
        """
        Writes the current state of the session key.

        Returns:
            None
        """
        st.write(st.session_state[self.key])
