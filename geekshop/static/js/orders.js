window.onload = function () {


    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost
    let quantity_arr = []
    let price_arr = []

    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val())

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0

    for (let i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val())
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'))
        quantity_arr[i] = _quantity
        if (_price) {
            price_arr[i] = _price
        } else {
            price_arr[i] = 0
        }
    }


    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target

        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''))
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value)
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num]
            quantity_arr[orderitem_num] = orderitem_quantity
            order_summary_update(price_arr[orderitem_num], delta_quantity)
        }

    })

    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''))
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num]
        } else {
            delta_quantity = quantity_arr[orderitem_num]
        }
        order_summary_update(price_arr[orderitem_num], delta_quantity)
    })

    function order_summary_update(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2))
        order_total_quantity = order_total_quantity + delta_quantity

        $('.order_total_quantity').html(order_total_quantity).toString()
        $('.order_total_cost').html(order_total_cost).toString()
    }

    $('.order_form').on('change', 'select', function () {
        let target = event.target
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''))
        let product_pk = target.value
        let data = {
            pk: product_pk
        }
        if (product_pk) {
            $.ajax({
                url: "/order/edit/" + product_pk + '/price/',
                data: data,
                success: function (data) {
                    if (data.price) {
                        price_arr[orderitem_num] = parseFloat(data.price)
                        let length_arr_formset = price_arr.length
                        let tr_for_price = $('.order_form table').find('tr:eq(' + length_arr_formset + ')')
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0
                            tr_for_price.find('input[type="number"]').val(quantity_arr[orderitem_num])
                        }
                        let html_price = '<span>' + data.price.toString() + '</span> руб'
                        tr_for_price.find('td:eq(2)').html(html_price)


                    }
                }
            })
        }


    })

    function delete_order_item(row) {
        let target_name = row[0].querySelector('input[type=number]').name
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''))
        delta_quantity = -quantity_arr[orderitem_num]
        order_summary_update(price_arr[orderitem_num], delta_quantity)

    }

    $('.formset_row').formset({
        addText: 'Добавить товар',
        deleteText: 'Удалить товар',
        prefix: 'orderitems',
        removed: delete_order_item
    })


}

