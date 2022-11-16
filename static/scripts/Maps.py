def generate_delay_map(selected_year, selected_type, selected_supplier, selected_day_limit):
    HtmlFile = open('./templates/maps/delay_maps/score_{}-{}-{}-{}.html'.format(selected_year, selected_type, selected_supplier, selected_day_limit), 'r', encoding='utf-8')
    
    source_code = HtmlFile.read()
    
    return source_code


def generate_queue_map(selected_year, selected_payment_type, selected_day):
    HtmlFile = open('./templates/maps/queues_maps/payment_queues_map_{}_{}_{}.html'.format(selected_year, selected_payment_type,selected_day), 'r', encoding='utf-8')
    
    source_code = HtmlFile.read()
    
    return source_code