import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import logging
import statistics
import itertools
import six

def get_fill_color_grayscale(num_traces):
    fill_colors = []
    offset = 10
    gap = (255-offset*2)/num_traces
    for i in range(num_traces):
        gray = i*gap + offset
        fill_colors.append("rgb({}, {}, {})".format(gray, gray,gray))
    return fill_colors


def plot_bdc(filename, stages, util_vals_dict, style=0):
    #
    # `util_vals_dict` should of the form:
    #       util_vals_dict = {"cpu": [a1, b1, ..., d1],
    #                         "gpu": [a2, b2, ..., d2],
    #                                   ...
    #                         "gpu": [aM, bM, ..., dM]}
    #
    # `stages` should be of form:
    #       stages = ["S1", "S2", ..., "SN"]
    #

    hws = list(util_vals_dict.keys())
    data = util_vals_dict.values()
    data_t = list(map(list, zip(*data)))

    # fill_colors array size must match size of stages array
    fill_colors = get_fill_color_grayscale(len(data_t))

    fig = go.Figure()
    for i in range(len(data_t)):
        fig.add_trace(go.Bar(
            name=stages[i], x=data_t[i],  y=hws, orientation='h',
            marker=dict(color=fill_colors[i],
                        line=dict(color='black', width=0)),
            ))

    if style is 0:
        # Fonts
        axis_title_font = dict(size=12, family='Calibri', color='black')
        axis_tick_font=dict(size=12, family='Calibri', color='black')
        legend_font=dict(size=12, family='Calibri', color='black')

        # Hard code bar widths and chart height depending on number of bars
        h_setting = dict()
        h_setting["height"] = 120 + 33*(len(hws)-1)
        h_setting["leg_y"] = [0, 0, 2.03, 1.65, 1.5, 1.39, 1.30][len(hws)]

        # Change the bar mode
        fig.update_layout(barmode='stack', plot_bgcolor='white',
                # Bar width and chart size settings
                width=400, height=h_setting["height"], bargap=0.25,

                # Axis settings
                xaxis=dict(title_text='Backend Development Cost', 
                            showline=True, linewidth=2, linecolor='black',
                            title_font=axis_title_font, tickfont=axis_tick_font),
                yaxis=dict(showline=True, linewidth=2, linecolor='black',
                            title_font=axis_title_font, tickfont=axis_tick_font),
                margin=dict(t=0, b=40, l=0, r=20),

                # Legend settings
                legend=dict(font=legend_font, orientation="h", traceorder='normal',
                            bordercolor="Black", borderwidth=1, 
                            y=h_setting["leg_y"], x=0.5,
                            xanchor='center', yanchor="top"))

    elif style is 1:
    
       # Fonts
        axis_title_font = dict(size=12, family='Calibri', color='black')
        axis_tick_font=dict(size=11, family='Calibri', color='black')
        legend_font=dict(size=8, family='Calibri', color='black')

        # Change the bar mode
        fig.update_layout(barmode='stack', plot_bgcolor='white',
                # Bar width and chart size settings
                width=400, height=120, bargap=0.25,

                # Axis settings
                xaxis=dict(title_text='Backend Development Cost', 
                            showline=True, linewidth=2, linecolor='black',
                            title_font=axis_title_font, tickfont=axis_tick_font
                            ),
                yaxis=dict(showline=True, linewidth=2, linecolor='black',
                            title_font=axis_title_font, tickfont=axis_tick_font,
                            ),
                margin=dict(t=5, b=40, l=0, r=0),

                # Legend settings
                legend=dict(font=legend_font, orientation="h", traceorder='normal',
                            bordercolor="Black", borderwidth=0,
                            y=1.5, x=0.5,
                            xanchor='center', yanchor="top"))

    elif style is 2:
        # Fonts
        axis_title_font = dict(size=12, family='Calibri', color='black')
        axis_tick_font=dict(size=12, family='Calibri', color='black')
        legend_font=dict(size=10, family='Calibri', color='black')

        # Change the bar mode
        fig.update_layout(barmode='stack', plot_bgcolor='white',
                # Bar width and chart size settings
                width=400, height=140, bargap=0.25,

                # Axis settings
                xaxis=dict(title_text='Backend Development Cost', 
                            showline=True, linewidth=2, linecolor='black',
                            title_font=axis_title_font, tickfont=axis_tick_font),
                yaxis=dict(showline=True, linewidth=2, linecolor='black',
                            title_font=axis_title_font, tickfont=axis_tick_font),
                margin=dict(t=5, b=40, l=0, r=0),

                # Legend settings
                legend=dict(font=legend_font, orientation="v", traceorder='normal',
                            bordercolor="Black", borderwidth=0))

    elif style is 3:
        # Fonts
        axis_title_font = dict(size=12, family='Calibri', color='black')
        axis_tick_font=dict(size=12, family='Calibri', color='black')
        legend_font=dict(size=10, family='Calibri', color='black')

        # Change the bar mode
        fig.update_layout(barmode='stack', plot_bgcolor='white',
                # Bar width and chart size settings
                width=400, height=180, bargap=0.25,

                # Axis settings
                xaxis=dict(title_text='Backend Development Cost', 
                            showline=True, linewidth=2, linecolor='black',
                            title_font=axis_title_font, tickfont=axis_tick_font),
                yaxis=dict(showline=True, linewidth=2, linecolor='black',
                            title_font=axis_title_font, tickfont=axis_tick_font),
                margin=dict(t=5, b=40, l=0, r=0),

                # Legend settings
                legend=dict(font=legend_font, orientation="v", traceorder='normal',
                            bordercolor="Black", borderwidth=0, 
                            y=0.1, x=1, 
                            xanchor='right', yanchor="bottom"))

    # To generate HTML output:
    pio.write_html(fig, file=filename + ".html",
                        auto_open=False, include_plotlyjs="cdn")

    logging.info("Plot generated at: {}".format(filename))

    # To generate image file output:
    fig.write_image(filename + ".pdf")
    
    logging.info("Plot generated at: {}".format(filename))


def plot_category_bdc(filename, categories, util_vals_dict):
    #
    # `util_vals_dict` should of the form:
    #       util_vals_dict = {"cpu": [[a1, b1, ..., d1], [a1, b1, ..., d1], ..., [a1, b1, ..., d1]],
    #                         "gpu": [[a2, b2, ..., d2], [a2, b2, ..., d2], ..., [a2, b2, ..., d2]],
    #                                   ...
    #                         "gpu": [[aM, bM, ..., dM], [aM, bM, ..., dM], ..., [aM, bM, ..., dM]}
    #
    # `stages` should be of form:
    #       stages = ["S1", "S2", ..., "SN"]
    #

    # Squash individual stage BDCs into 1 bdc per category
    data = []
    for (_,hw) in util_vals_dict.items():
        accs = []
        for cat in hw:
            acc = 0
            for stage in cat:
                acc += stage
            accs.append(acc)
        data.append(accs)

    hws = list(util_vals_dict.keys())

    # Wrap around first category
    categories.append(categories[0])

    # Markers
    symbols=['triangle-se-open', 'square-open', 'cross-thin-open', 'circle-open', 'diamond-open', 'hexagon2']
    lines=['solid', 'dot', 'dash', 'dashdot', 'longdash', '5px 10px 2px 2px']
    #colors=['rgb(128, 0, 0)', 'rgb(250, 190, 190)', 'rgb(255, 225, 25)', 'rgb(0, 0, 0)']

    fig = go.Figure()
    for i in range(len(hws)):

        # Wrap around first data point
        data[i].append(data[i][0])

        fig.add_trace(go.Scatterpolar(
            name=hws[i],
            r=data[i],
            theta=categories,
            #fill='toself',
            marker=dict(symbol=symbols[i], size=12),
            #line=dict(dash="solid", width=2),
            line=dict(dash=lines[i], width=2),
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
        showlegend=True,

        width=500, height=500,
        margin=dict(t=0, b=0, l=70, r=70),
        
         # Legend settings
        legend=dict(font=legend_font, bordercolor="Black",
                    borderwidth=2, orientation="h",
                    xanchor='center', y=0, x=0.5))

    # To generate HTML output:
    pio.write_html(fig, file=filename + ".html",
                        auto_open=False, include_plotlyjs="cdn")

    logging.info("Plot generated at: {}".format(filename))

    # To generate image file output:
    fig.write_image(filename + ".pdf")
    
    logging.info("Plot generated at: {}".format(filename))



def gen_latex_table(ftt, filename):
    
    # Define function to generate output for one feature
    def gen_mask_str(mask):
        # out = ""
        # for i in range(len(mask)):
        #     out += (r"\hspace{0.30mm}\uparrow\hspace{0.1mm}" if mask[i].value == 1 else " - ")
        #     if i < (len(mask) - 1):
        #         out += ","

        # out = "${[}"+ out +"{]}$"
        out = ""
        for i in range(len(mask)):
            out += str(mask[i])
            if i < (len(mask) - 1):
                out += ","

        out = "["+ out +"]"

        return out

    def gen_feature_str(feature, level):
        out = r"\hspace{" + str(level*3) +"mm} "
        out += "{} & {} & {} & {} & {} & {} \\\\ \n\n".format(
            feature.longname,
            feature.description,
            gen_mask_str(feature.stage_mask) if feature.is_leaf_node() else "",
            str(feature.combine).capitalize() if not feature.is_leaf_node() else "",
            "{:0.1f}".format(feature.weight),
            feature.scale if feature.is_leaf_node() else "",
            )

        return out

    # Generate file
    with open(filename, "w+") as file:

        # Header
        file.write(r'''
\centering
\begin{tabularx}{\textwidth}{@{}lXcccc@{}}
\toprule
\multicolumn{1}{c}{Feature Name} & 
\multicolumn{1}{c}{Brief Description} & 
\multicolumn{1}{c}{Stage Mask} & 
\multicolumn{1}{c}{Combine} & 
\multicolumn{1}{c}{Weight} & 
\multicolumn{1}{c}{Scale} \\ \midrule
'''         )

        file.write(gen_feature_str(ftt.root, 0))

        # file.write("\hdashline[3pt/1pt]\n")
        memory = ftt.find_sub_f("system.memory")[0]
        file.write(gen_feature_str(memory, 1))
        [file.write(gen_feature_str(f, 2)) for f in memory.find_sub_f("memory.*")]

        # file.write("\hdashline[3pt/1pt]\n")
        nodes = ftt.find_sub_f("system.nodetypes_set.node")[0]
        file.write(gen_feature_str(nodes, 1))
        control = nodes.find_sub_f("node.control")[0]
        file.write(gen_feature_str(control, 2))
        [file.write(gen_feature_str(f, 3)) for f in control.find_sub_f("control.*")]
        data_mov = nodes.find_sub_f("node.data_mov")[0]
        file.write(gen_feature_str(data_mov, 2))
        [file.write(gen_feature_str(f, 3)) for f in data_mov.find_sub_f("data_mov.*")]
        datapath = nodes.find_sub_f("node.datapaths_set.datapath")[0]
        file.write(gen_feature_str(datapath, 2))
        [file.write(gen_feature_str(f, 3)) for f in datapath.find_sub_f("datapath.*")]

        # file.write("\hdashline[3pt/1pt]\n")
        network = ftt.find_sub_f("system.network")[0]
        file.write(gen_feature_str(network, 1))
        [file.write(gen_feature_str(f, 2)) for f in network.find_sub_f("network.*")]

        # Footer
        file.write(r'''
\bottomrule
\end{tabularx}
'''         )

    logging.info("Generated HW Feature Tree latex table at: " + filename)



def plot_user_study_bw(filename, dataset):

    # fill_colors array size must match size of stages array
    fill_colors = [ "rgba(0, 0, 0, 0.10)",
                    "rgba(0, 0, 0, 0.35)",
                    "rgba(0, 0, 0, 0.7)",
                    "rgba(0, 0, 0, 0.85)"]

    dataset_t = list(map(list, zip(*dataset)))
    dataset_t.sort(key=statistics.mean)
    print(dataset_t)
    fig = go.Figure()
    for i in range(len(dataset_t)):
        fig.add_trace(go.Box(name="{}".format(i), y=dataset_t[i],
                                marker_color='black', marker_size=2,
                                whiskerwidth=0.8,
                                #jitter=0.3,
                                line_width=1))

    # # Fonts
    axis_title_font = dict(size=14, family='Calibri', color='black')
    axis_tick_font=dict(size=14, family='Calibri', color='black')
    
    # Change the bar mode
    fig.update_layout(plot_bgcolor='white',
            # Bar width and chart size settings
            width=450, height=230,

            # # Axis settings
            xaxis=dict(title_text='Prompt Number', 
                        showline=True, linewidth=2, linecolor='black',
                        title_font=axis_title_font, tickfont=axis_tick_font,
                        dtick=1),
            yaxis=dict(title_text='Likert Scale Score', 
                        showline=True, linewidth=2, linecolor='black',
                        showgrid=False, gridcolor='black', gridwidth=1,
                        title_font=axis_title_font, tickfont=axis_tick_font,
                        range=[0.5,5.5]),
            margin=dict(t=0, b=50, l=40, r=0),
            
            showlegend=False)


    # To generate HTML output:
    pio.write_html(fig, file=filename + ".html",
                        auto_open=False, include_plotlyjs="cdn")

    # logging.info("Plot generated at: {}".format(filename))

    # To generate image file output:
    fig.write_image(filename + ".pdf")
    
    logging.info("Plot generated at: {}".format(filename))



def plot_user_study_sb(filename, dataset):

    # fill_colors array size must match size of stages array
    fill_colors = [ "rgba(0, 0, 0, 0.05)",
                    "rgba(0, 0, 0, 0.25)",
                    "rgba(0, 0, 0, 0.6)",
                    "rgba(0, 0, 0, 0.80)",
                    "rgba(0, 0, 0, 1)"]

    questions = list(map(list, six.moves.zip_longest(*dataset, fillvalue='-')))
    print("Questions:")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in questions]))
    main_q = questions.pop(14)

    # remove last question about DMA
    questions.pop()

    questions.sort(key=statistics.mean, reverse=True)
    questions.append([0]*len(main_q))
    questions.append(main_q)

    print("Final Questions:")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in questions]))

    ticktexts = []
    for i in range(len(questions)-2):
        ticktexts.append(str(i))
    ticktexts.append("")
    ticktexts.append("A")

    tickval = [i for i in range(len(questions))]

    means = [ [], [], [], [], [] ]
    for q in questions:
        maximum = max(q)
        for i in range (len(means)):
            if i == maximum - 1:
                means[i].append("{:0.1f}".format(statistics.mean(q)))
            else:
                means[i].append("")

    groups = [ [], [], [], [], [] ]
    for i in range(len(questions)):
        # For each question array in questions[i]
        for g in range(len(groups)):
            # Get number of cells with value of g+1 
            val = questions[i].count(g+1)

            # normalize value by total cells for this question
            val = val / len(questions[i])

            groups[g].append(val)

    # # Fonts
    axis_title_font = dict(size=14, family='Calibri', color='black')
    axis_tick_font=dict(size=14, family='Calibri', color='black')
    axis_tick_font_y=dict(size=10, family='Calibri', color='black')
    text_font=dict(size=14, family='Calibri', color='black')
    legend_font = dict(size=9, family='Calibri', color='black')
    

    options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    fig = go.Figure()
    for i in range(len(groups)):
        fig.add_trace(go.Bar(
            name=options[i], y=groups[i],
            marker=dict(color=fill_colors[i],
                         line=dict(color='black', width=0)),
            text=means[i], textposition='outside', textfont=text_font
            ))

    # Change the bar mode
    fig.update_layout(barmode='stack', plot_bgcolor='white', bargap=0.3,
            # Bar width and chart size settings
            width=450, height=240,

            # # Axis settings
            xaxis=dict(title_text='Question Number', 
                        showline=True, linewidth=2, linecolor='black',
                        title_font=axis_title_font, tickfont=axis_tick_font,
                        dtick=1,
                        ticktext=ticktexts, tickvals=tickval),
            yaxis=dict(title_text='Responses', 
                        showline=True, linewidth=2, linecolor='black',
                        showgrid=False, gridcolor='black', gridwidth=1,
                        title_font=axis_title_font,
                        tickfont=axis_tick_font_y, tickformat="%", dtick=0.50,
                        ticks='outside',
                        range=[0, 1.19] ),
            margin=dict(t=0, b=40, l=0, r=0),

            annotations=[
                go.layout.Annotation(
                    x=13,
                    y=1.12,
                    xref="x",
                    yref="y",
                    text="Avg Score",
                    showarrow=True,
                    arrowhead=1,
                    ax=13,
                    ay=-15,
                    font=legend_font,
                    arrowcolor="black"
                )
            ],

            legend=dict(font=legend_font, bordercolor="black",
                        borderwidth=0, orientation="h",
                        xanchor='center', y=1.25, x=0.5))


    # To generate HTML output:
    pio.write_html(fig, file=filename + ".html",
                        auto_open=False, include_plotlyjs="cdn")

    # logging.info("Plot generated at: {}".format(filename))

    # To generate image file output:
    fig.write_image(filename + ".pdf")
    
    logging.info("Plot generated at: {}".format(filename))



def plot_category_bdc_bars(filename, categories, util_vals_dict, style=0):
    #
    # `util_vals_dict` should of the form:
    #       util_vals_dict = {"cpu": [[a1, b1, ..., d1], [a1, b1, ..., d1], ..., [a1, b1, ..., d1]],
    #                         "gpu": [[a2, b2, ..., d2], [a2, b2, ..., d2], ..., [a2, b2, ..., d2]],
    #                                   ...
    #                         "gpu": [[aM, bM, ..., dM], [aM, bM, ..., dM], ..., [aM, bM, ..., dM]}
    #
    # `stages` should be of form:
    #       stages = ["S1", "S2", ..., "SN"]
    #

    # Squash individual stage BDCs into 1 bdc per category
    data = []
    for (_,hw) in util_vals_dict.items():
        accs = []
        for cat in hw:
            acc = 0
            for stage in cat:
                acc += stage
            accs.append(acc)
        data.append(accs)

    hws = list(util_vals_dict.keys())

    # colors
    fill_colors = get_fill_color_grayscale(len(hws))

    symbols=['triangle-se-open', 'square-open', 'cross-thin-open', 'circle-open', 'diamond-open', 'hexagon2']

    fig = go.Figure()
    for i in range(len(hws)):

        fig.add_trace(go.Bar(
            x=categories, y=data[i], name=hws[i],
            marker=dict(color=fill_colors[i], #symbol=symbols[i],
                        line=dict(color='black', width=0))
            ))
    if style is 0:
        # Fonts
        axis_tick_font=dict(size=12, family='Calibri', color='black')
        legend_font=axis_tick_font
        axis_title_font = axis_tick_font

        fig.update_layout( 
            barmode='group',
            bargap=0.3,
            plot_bgcolor='white',
            showlegend=True,

            width=400, height=300 if len(hws) is 4 else 318,
            margin=dict(t=10, b=80, l=40, r=0),

            xaxis=dict(#title_text='BDC Categories', 
                        showline=True, linewidth=2, linecolor='black',
                        title_font=axis_title_font, tickfont=axis_tick_font
                        ),

            yaxis=dict(title_text='Backend Development Cost', 
                        showline=True, linewidth=2, linecolor='black',
                        showgrid=False, gridcolor='black', gridwidth=1,
                        title_font=axis_title_font,
                        tickfont=axis_tick_font),

            # Legend settings
            legend=dict(font=legend_font, bordercolor="Black",
                        borderwidth=2, orientation="h",
                        xanchor='center', y=-0.15, x=0.5,
                        ))
    elif style is 2:
       # Fonts
        axis_tick_font=dict(size=12, family='Calibri', color='black')
        legend_font=dict(size=10, family='Calibri', color='black')
        axis_title_font = axis_tick_font

        fig.update_layout( 
            barmode='group',
            bargap=0.3,
            plot_bgcolor='white',
            showlegend=True,

            width=400, height=210,
            margin=dict(t=5, b=40, l=40, r=0),

            xaxis=dict(title_text='Hardware Feature Categories', 
                        showline=True, linewidth=2, linecolor='black',
                        title_font=axis_title_font, tickfont=axis_tick_font
                        ),

            yaxis=dict(title_text='Backend Development Cost', 
                        showline=True, linewidth=2, linecolor='black',
                        showgrid=False, gridcolor='black', gridwidth=1,
                        title_font=axis_title_font,
                        tickfont=axis_tick_font),

            # Legend settings
            legend=dict(font=legend_font, bordercolor="Black",
                        borderwidth=0, orientation="v",
                        xanchor='right', y=1, x=1,
                        ))

    elif style is 3:
       # Fonts
        axis_tick_font=dict(size=12, family='Calibri', color='black')
        legend_font=dict(size=10, family='Calibri', color='black')
        axis_title_font = axis_tick_font

        fig.update_layout( 
            barmode='group',
            bargap=0.3,
            plot_bgcolor='white',
            showlegend=True,

            width=400, height=220,
            margin=dict(t=5, b=40, l=40, r=0),

            xaxis=dict(title_text='Hardware Feature Categories', 
                        showline=True, linewidth=2, linecolor='black',
                        title_font=axis_title_font, tickfont=axis_tick_font
                        ),

            yaxis=dict(title_text='Backend Development Cost', 
                        showline=True, linewidth=2, linecolor='black',
                        showgrid=False, gridcolor='black', gridwidth=1,
                        title_font=axis_title_font,
                        tickfont=axis_tick_font),

            # Legend settings
            legend=dict(font=legend_font, bordercolor="Black",
                        borderwidth=0, orientation="h",
                        xanchor='left', y=1, x=0.01,
                        ))

    # To generate HTML output:
    pio.write_html(fig, file=filename + ".html",
                        auto_open=False, include_plotlyjs="cdn")

    logging.info("Plot generated at: {}".format(filename))

    # To generate image file output:
    fig.write_image(filename + ".pdf")
    
    logging.info("Plot generated at: {}".format(filename))