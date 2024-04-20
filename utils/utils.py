import streamlit as st


class SessionState:

    def __init__(self, key: str, default_state: bool = False):
        self.key = key
        self.default_state = default_state

        if self.key not in st.session_state:
            st.session_state[self.key] = self.default_state

    def sessionstate_true(self) -> None:
        """
        Sets the value of the specified key in the session state to True.

        Parameters:
            key (str): The key to set in the session state.

        Returns:
            None
        """
        st.session_state[self.key] = True

    def sessionstate_false(self) -> None:
        """
        Sets the value of the specified key in the session state to True.

        Parameters:
            key (str): The key to set in the session state.

        Returns:
            None
        """
        st.session_state[self.key] = False

    def check_sessionstate(self) -> bool:
        """
        Returns the value of the specified key in the session state.

        Parameters:
            key (str): The key to check in the session state.

        Returns:
            bool: The value of the specified key in the session state.
        """
        return st.session_state[self.key]

    def write_currentstate(self) -> None:
        """
        Writes the current state of the session key.
        """
        st.write(st.session_state[self.key])
