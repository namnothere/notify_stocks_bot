def get_xpath_ids():
    data_set = [
        # 1. Khung ngang của 4 chart pie
        {
            'xPathId': 2,
            'title': '4_CHART_PIE',
            'status': 1
        },
        # 2. Khung thông tin chung
        {
            'xPathId': 3,
            'title': 'GENERAL_INFORMATION',
            'status': 0
        },
        # 3. Khung định giá cổ phiếu
        {
            'xPathId': 5,
            'title': 'STOCK_VALUATION',
            'status': 1
        },
        # 4. Khung Xếp hạng nhóm ngành
        {
            'xPathId': 7,
            'title': 'INDUSTRY_GROUP_RANKING',
            'status': 0
        },
        # 5. Khung Xếp hạng cổ phiếu
        {
            'xPathId': 8,
            'title': 'STOCK_RATING',
            'status': 0
        },
        # 6. Khung Chỉ số tài chính
        {
            'xPathId': 9,
            'title': 'FINANCIAL_INDICATORS',
            'status': 0
        },
        # 7. Khung Chỉ số Kỹ thuật
        {
            'xPathId': 10,
            'title': 'TECHNICAL_INDICATORS',
            'status': 0
        }
    ]

    xPathIds = []
    for element in data_set:
        if element['status'] == 1:
            xPathIds.append(element['xPathId'])
    return xPathIds
