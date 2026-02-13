"""Streamlit entrypoint for the minimal provider example."""

from renderflow.streamlit_renderer import run_renderer


def main():
    # Module name works without requiring entrypoint package installation.
    run_renderer("minimal_provider")


if __name__ == "__main__":
    main()
