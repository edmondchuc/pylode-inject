import click
from bs4 import BeautifulSoup

import yaml


def add_logo(soup, config):
    # Insert Logo before the ontology title.
    logo_a = soup.new_tag('a', href=config['logo']['href'])
    logo_image = soup.new_tag('img', src=config['logo']['src'], )
    logo_image['alt'] = config['logo']['alt']
    logo_a.insert(1, logo_image)
    soup.div.insert_after("", logo_a)
    return soup


def add_overview_to_toc(soup):
    # Add Overview section to the table of contents.
    toc_li = soup.new_tag('li')
    toc_a = soup.new_tag('a', href='#overview')
    toc_a.insert(1, 'Overview')
    toc_li.insert(1, toc_a)
    for section in soup.find_all('section'):
        if section['id'] == 'toc':
            section.ol.insert(1, toc_li)
    return soup


def add_figures_opening_paragraph(soup, config):
    # Add the opening paragraph describing the following figures.
    for section in soup.find_all('section'):
        if section['id'] == 'overview':
            # Figure paragraph.
            figure_p = soup.new_tag('p')
            figure_p.string = config['overview']['p']
            figure_p['style'] = 'padding-bottom: 1rem;'
            section.append(figure_p)

            # Remove the div with class "figure" generated by pyLODE.
            section.div.extract()
    return soup


def add_figures(soup, config):
    # Add figures to the Overview section.
    for section in soup.find_all('section'):
        if section['id'] == 'overview':

            for i, figure in enumerate(config['overview']['figures'], start=1):
                # Add image to figure tag.
                figure = figure['figure']
                figure_tag = soup.new_tag('figure')

                figure_img_tag = soup.new_tag('img', src=figure['src'])
                figure_img_tag['alt'] = figure['alt']
                figure_tag.append(figure_img_tag)

                # Add caption to figure tag.
                figure_caption_tag = soup.new_tag('figcaption')
                figure_strong_tag = soup.new_tag('strong')
                figure_strong_tag.string = 'Figure {}: '.format(i)
                figure_caption_tag.insert(1, figure_strong_tag)
                figure_strong_tag.insert_after(figure['caption'])
                figure_img_tag.insert_after(figure_caption_tag)
                figure_caption_tag['style'] = 'padding-bottom: 3rem'

                section.append(figure_tag)

    return soup


def add_figures_to_classes(soup, config, figures_count):
    for i, figure in enumerate(config['classes']['figures'], start=figures_count+1):
        figure = figure['figure']
        for div in soup.find_all('div'):
            if div['id'] == figure['id']:
                # Add image to figure tag.
                figure_tag = soup.new_tag('figure')
                div.insert(2, figure_tag)
                figure_img_tag = soup.new_tag('img', src=figure['src'])
                figure_img_tag['alt'] = figure['alt']
                figure_tag.append(figure_img_tag)

                # Add caption to figure tag.
                figure_caption_tag = soup.new_tag('figcaption')
                figure_strong_tag = soup.new_tag('strong')
                figure_strong_tag.string = 'Figure {}: '.format(i)
                figure_caption_tag.insert(1, figure_strong_tag)
                figure_strong_tag.insert_after(figure['caption'])
                figure_img_tag.insert_after(figure_caption_tag)
                figure_caption_tag['style'] = 'padding-bottom: 3rem'

                div.append(figure_tag)
    return soup


@click.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.argument('html_file', type=click.Path(exists=True))
@click.argument('output_html_file', type=click.Path())
def inject(config_file, html_file, output_html_file):
    """Inject logo images, links, paragraphs, and figures to a pyLODE document.\n
    CONFIG_FILE: The YAML-based configuration file.\n
    HTML_FILE: The pyLODE HTML file.\n
    OUTPUT_HTML_FILE: The file output with the injected result."""
    with open(config_file) as f:
        config = yaml.safe_load(f)

    with open(html_file) as f:
        soup = BeautifulSoup(f, 'html.parser')

        click.echo('Adding logo...')
        soup = add_logo(soup, config)

        click.echo('Adding overview to table of contents...')
        soup = add_overview_to_toc(soup)

        click.echo('Adding opening paragraph of figures section...')
        soup = add_figures_opening_paragraph(soup, config)

        click.echo('Adding figures to the figures section...')
        soup = add_figures(soup, config)

        click.echo('Adding figures to classes and properties...')
        figures_count = len(config['overview']['figures'])
        soup = add_figures_to_classes(soup, config, figures_count)

    # Write processed HTML to file.
    click.echo('Writing to disk...')
    with open(output_html_file, 'w') as f:
        # Output with formatter=None to not escape HTML in strings.
        f.writelines(str(soup.prettify(formatter=None)))

    click.echo('Output file: {}'.format(output_html_file))
    click.echo('Finished.')


if __name__ == '__main__':
    inject()