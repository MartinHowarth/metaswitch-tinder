import dash_html_components as html


def create_equal_grid(elements):
    """

    :param elements: List of rows, of which each is a list of columns
        Rows must be of equal length.
        Each element of a row must be a html.Div.
    :return:
    """
    n_columns = len(elements[0])

    if not all([len(row) == n_columns for row in elements]):
        raise ValueError("Not all rows are of the same length.")

    # Bootstrap allows a maximum of 12 columns per grid.
    column_class = "col-sm-{}".format(int(12 / n_columns))

    grid_children = []
    for row in elements:
        row_children = []
        for col in row:
            if hasattr(col, "className"):
                col.className += " {}".format(column_class)
            else:
                col.className = column_class
            row_children.append(col)

        grid_children.append(html.Div(children=row_children, className="row"))

    grid = html.Div(children=grid_children, className="container")
    return grid


def create_equal_row(elements):
    return create_equal_grid([elements])


def create_magic_three_grid(elements):
    """

    :param elements: List of rows, of which each is a list of columns
        Rows must be of equal length.
        Each element of a row must be a html.Div.
    :return:
    """
    n_columns = len(elements[0])

    if not all([len(row) == n_columns for row in elements]):
        raise ValueError("Not all rows are of the same length.")

    grid_children = []
    for row in elements:
        row_children = []
        for num, col in enumerate(row):
            if (num == 0) or (num == 2):
                column_class = "col-sm-2 align-middle"
            elif num == 1:
                column_class = "col-sm-4 align-middle"
            else:
                break

            if hasattr(col, "className"):
                col.className += " {}".format(column_class)
            else:
                col.className = column_class
            row_children.append(col)

            if (num == 0) or (num == 1):
                row_children.append(html.Div("", className="col-sm-2"))

        grid_children.append(html.Div(children=row_children, className="row"))

    grid = html.Div(children=grid_children, className="container")
    return grid


def create_magic_three_row(elements):
    return create_magic_three_grid([elements])
