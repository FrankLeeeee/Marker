def post_process(result):
    coordinates = result[0]
    max_y = 0
    min_y = float('inf')
    min_x = float('inf')

    for coordinate in coordinates:
        if coordinate[1] > max_y:
            max_y = coordinate[1]

        if coordinate[1] < min_y:
            min_y = coordinate[1]

        if coordinate[0] < min_x:
            min_x = coordinate[0]

    text = result[1]

    KEYWORDS = ['我的评分', '分钟', '上映日期', '动作', '观影时间']

    for keyword in KEYWORDS:
        if keyword in text:
            return (None, None, None)

    if max_y - min_y < 60 or min_x < 280 or min_x > 295:
        result = (None, None, None)
    return result
