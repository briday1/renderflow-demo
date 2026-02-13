"""Streamlit entrypoint for the minimal provider example."""

from renderflow.streamlit_renderer import run_renderer


def main():
    # Entrypoint name resolved from pyproject registration.
    run_renderer("minimal-provider")


if __name__ == "__main__":
    main()
