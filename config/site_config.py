"""
This file contains the site configuration for the project

The `div_configs` dictionary stores CSS styles that can be used to hide certain elements on the
site.
"""

div_configs = {
    "hide_expander": """
                    <style>
                        [data-testid="collapsedControl"] {
                            display: none
                        }
                    </style>""",
    "hide_github_icon": """
                    <style>
                    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
                    </style>""",
    "hide_streamlit_style": """
                    <style>
                    #MainMenu { visibility: hidden; }
                    footer { visibility: hidden; }
                    </style>""",
}
