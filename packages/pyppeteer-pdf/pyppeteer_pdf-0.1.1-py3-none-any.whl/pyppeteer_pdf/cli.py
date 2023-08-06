import asyncio
import tempfile

import click
from click.utils import LazyFile

from pyppeteer import launch


@click.command()
@click.argument("source")
@click.argument("filename", required=False, type=click.File("wb"))
@click.option("--html", is_flag=True, default=False, help="The source is html")
@click.option(
    "--print", "print_style", is_flag=True, default=False, help="Use print stylesheets."
)
@click.option(
    "-pb/--printBackground",
    is_flag=True,
    default=False,
    help="Print background graphics.",
)
@click.option("--format", default="Letter")
def html2pdf_command(*args, **kwargs):
    asyncio.get_event_loop().run_until_complete(html2pdf(**kwargs))


async def html2pdf(source, html, print_style, filename, pb, format):
    browser = await launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
    page = await browser.newPage()

    if html:
        await page.setContent(source)
    else:
        await page.goto(source)

    if print_style is not True:
        await page.emulateMedia("screen")

    if filename is None:
        filename = tempfile.mktemp()
    else:
        filename = filename.name

    await page.pdf({"path": filename, "format": format, "printBackground": pb})
    await browser.close()

    click.echo(click.style(filename, fg="green"))


if __name__ == "__main__":
    html2pdf_command()
