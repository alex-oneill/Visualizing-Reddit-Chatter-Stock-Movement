class ChartVal:
    def __init__(self):
        self.group_times = []
        self.group_comments = []
        self.group_points = []
        self.group_ticker = []
        self.group_price = []
        self.group_volume = []

    def __str__(self) -> str:
        text_dict = {'start_times': str(self.group_times),
                     'comments_counts': str(self.group_comments),
                     'points': str(self.group_points),
                     'price': str(self.group_price),
                     'volume': str(self.group_volume)}
        return str(text_dict)

    def return_chart_vals(self) -> tuple:
        return self.group_times, self.group_points, self.group_price, self.group_volume

    def add_points(self, points_tup: dict) -> None:
        self.group_times.append(points_tup['start_time'])
        self.group_comments.append(points_tup['comment_count'])
        self.group_points.append(points_tup['group_points'])

    def add_stock(self, stock_tup: tuple) -> None:
        (_, end_price, end_volume) = stock_tup
        self.group_price.append(end_price)
        self.group_volume.append(end_volume)
