from fastui import AnyComponent
from fastui import components as c


def demo_page(title: str | None = None) -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Text(text="Hello, World!"),
            ]
        )
    ]