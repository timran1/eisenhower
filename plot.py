import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import logging
import statistics
import itertools
import six

def plot_experiment(filename, stages, eval_results, categories, category_results):
    plot_bdc(filename + "-stages", stages, eval_results)
    plot_category_bdc(filename + "-cats", categories, category_results)
    plot_category_bdc_bars(filename + "-cats-bars", categories, category_results)


def plot_bdc(filename, stages, bdc_vals_dict, style=0):
    #
    # `bdc_vals_dict` should of the form:
    #       bdc_vals_dict = {"cpu": [a1, b1, ..., d1],
    #                         "gpu": [a2, b2, ..., d2],
    #                                   ...
    #                         "gpu": [aM, bM, ..., dM]}
    #
    # `stages` should be of form:
    #       stages = ["S1", "S2", ..., "SN"]
    #

    hws = list(bdc_vals_dict.keys())
    data = bdc_vals_dict.values()
    data_t = list(map(list, zip(*data)))

    fig = go.Figure()
    for i in range(len(data_t)):
        fig.add_trace(go.Bar(
            name=stages[i], x=data_t[i],  y=hws, orientation='h'
            ))

    # Fonts
    axis_title_font = dict(size=12, family='Calibri', color='black')
    axis_tick_font=axis_title_font
    legend_font=axis_title_font

    # Change the bar mode
    fig.update_layout(barmode='stack',

            # Axis settings
            xaxis=dict(title_text='Backend Development Cost', 
                        showline=True, linewidth=2, linecolor='black',
                        title_font=axis_title_font, tickfont=axis_tick_font
                        ),
            yaxis=dict(showline=True, linewidth=2, linecolor='black',
                        title_font=axis_title_font, tickfont=axis_tick_font,
                        ))

    # To generate HTML output:
    pio.write_html(fig, file=filename + ".html",
                        auto_open=False, include_plotlyjs="cdn")

    logging.info("Plot generated at: {}".format(filename))

    # To generate image file output:
    fig.write_image(filename + ".pdf")
    
    logging.info("Plot generated at: {}".format(filename))


def plot_category_bdc(filename, categories, bdc_vals_dict):
    #
    # `bdc_vals_dict` should of the form:
    #       bdc_vals_dict = {"cpu": [[a1, b1, ..., d1], [a1, b1, ..., d1], ..., [a1, b1, ..., d1]],
    #                         "gpu": [[a2, b2, ..., d2], [a2, b2, ..., d2], ..., [a2, b2, ..., d2]],
    #                                   ...
    #                         "gpu": [[aM, bM, ..., dM], [aM, bM, ..., dM], ..., [aM, bM, ..., dM]}
    #
    # `stages` should be of form:
    #       stages = ["S1", "S2", ..., "SN"]
    #

    # Squash individual stage BDCs into 1 bdc per category
    data = []
    for (_,hw) in bdc_vals_dict.items():
        accs = []
        for cat in hw:
            acc = 0
            for stage in cat:
                acc += stage
            accs.append(acc)
        data.append(accs)

    hws = list(bdc_vals_dict.keys())

    # Wrap around first category
    categories.append(categories[0])

    fig = go.Figure()
    for i in range(len(hws)):

        # Wrap around first data point
        data[i].append(data[i][0])

        fig.add_trace(go.Scatterpolar(
            name=hws[i],
            r=data[i],
            theta=categories,
            mode='lines'
        ))

    # Fonts
    axis_tick_font=dict(size=14, family='Calibri', color='black')
    legend_font=axis_tick_font
    
    fig.update_layout(  
        polar=dict(
            radialaxis=dict(showticklabels=False, showline=False,
                            showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
            angularaxis = dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.3)',
                            tickfont=axis_tick_font),
            bgcolor='white'),
        showlegend=True)

    # To generate HTML output:
    pio.write_html(fig, file=filename + ".html",
                        auto_open=False, include_plotlyjs="cdn")

    logging.info("Plot generated at: {}".format(filename))

    # To generate image file output:
    fig.write_image(filename + ".pdf")
    
    logging.info("Plot generated at: {}".format(filename))


def plot_category_bdc_bars(filename, categories, bdc_vals_dict, style=0):
    #
    # `bdc_vals_dict` should of the form:
    #       bdc_vals_dict = {"cpu": [[a1, b1, ..., d1], [a1, b1, ..., d1], ..., [a1, b1, ..., d1]],
    #                         "gpu": [[a2, b2, ..., d2], [a2, b2, ..., d2], ..., [a2, b2, ..., d2]],
    #                                   ...
    #                         "gpu": [[aM, bM, ..., dM], [aM, bM, ..., dM], ..., [aM, bM, ..., dM]}
    #
    # `stages` should be of form:
    #       stages = ["S1", "S2", ..., "SN"]
    #

    # Squash individual stage BDCs into 1 bdc per category
    data = []
    for (_,hw) in bdc_vals_dict.items():
        accs = []
        for cat in hw:
            acc = 0
            for stage in cat:
                acc += stage
            accs.append(acc)
        data.append(accs)

    hws = list(bdc_vals_dict.keys())

    fig = go.Figure()
    for i in range(len(hws)):

        fig.add_trace(go.Bar(
            x=categories, y=data[i], name=hws[i]
            ))

    # Fonts
    axis_tick_font=dict(size=12, family='Calibri', color='black')
    legend_font=axis_tick_font
    axis_title_font = axis_tick_font

    fig.update_layout( 
        barmode='group',
        bargap=0.3,
        showlegend=True,

        xaxis=dict(#title_text='BDC Categories', 
                    showline=True, linewidth=2, linecolor='black',
                    title_font=axis_title_font, tickfont=axis_tick_font
                    ),

        yaxis=dict(title_text='Backend Development Cost', 
                    showline=True, linewidth=2, linecolor='black',
                    showgrid=False, gridcolor='black', gridwidth=1,
                    title_font=axis_title_font,
                    tickfont=axis_tick_font),
        )

    # To generate HTML output:
    pio.write_html(fig, file=filename + ".html",
                        auto_open=False, include_plotlyjs="cdn")

    logging.info("Plot generated at: {}".format(filename))

    # To generate image file output:
    fig.write_image(filename + ".pdf")
    
    logging.info("Plot generated at: {}".format(filename))
