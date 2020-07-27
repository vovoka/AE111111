from flask import render_template, redirect, url_for, request, current_app
from app import app
from app.forms import OrderRequestForm
from app.utils import (generate_sign, get_currency_code,
                       dict_values_concatenator)
import requests
import uuid
import logging
from decimal import Decimal

TIMEOUT_SEC = 6  # wait response for


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Service start page. Render WTForm. If the WTForm is submitted the
    form-data is transfered to one of 3 pay-channels
    depending of chosen currency
    """

    form = OrderRequestForm()
    if form.validate_on_submit():
        amount = form.amount.data.quantize(Decimal("1.00"))
        currency = request.form.get('currency')
        item_description = request.form.get('item_description')
        shop_order_id = uuid.uuid4()

        app.logger.info(
            f'{amount}|{currency}|{shop_order_id}|{item_description}')
        # choose pay channel by chosen currency code (978, 'EUR'), (840, 'USD')
        pay_channels = {
            'EUR': 'place_order_via_pay',
            'USD': 'place_order_via_bill',
        }
        currency_code = get_currency_code(currency)
        shop_id = current_app.config['SHOP_ID']
        pay_channel = pay_channels.get(currency) or 'place_order_via_invoice'
        return redirect(url_for(
            pay_channel,
            amount=amount,
            currency=currency_code,
            shop_order_id=shop_order_id,
            shop_id=shop_id,
        ))
    return render_template('index.html', form=form)


@app.route(
    '/place_order_via_pay/<amount>/<currency>/<shop_order_id>/<shop_id>',
    methods=['GET', 'POST'])
def place_order_via_pay(
        amount: str,
        currency: str,
        shop_order_id: uuid,
        shop_id: int):
    """
    Prepare expected data (required_keys) and render it at pay_form.html
    """

    data = locals()
    required_keys = ['amount', 'currency', 'shop_id', 'shop_order_id']
    sign_source_string = dict_values_concatenator(
        data, required_keys) + current_app.config['SECRET_KEY']
    data['sign'] = generate_sign(sign_source_string)
    return render_template('pay_form.html', **data)


@app.route(
    '/place_order_via_bill/<amount>/<currency>/<shop_order_id>/<shop_id>',
    methods=['GET', 'POST'])
def place_order_via_bill(
        amount: str,
        currency: str,
        shop_order_id: uuid,
        shop_id: int):
    """ Prepare data to send reqeust to url and returns responce(json) """

    data = {
        'payer_currency': int(currency),
        'shop_amount': amount,
        'shop_currency': currency,
        'shop_id': current_app.config['SHOP_ID'],
        'shop_order_id': shop_order_id,
    }
    required_keys = ['payer_currency', 'shop_amount',
                     'shop_currency', 'shop_id', 'shop_order_id']
    sign_source_string = (dict_values_concatenator(
        data, required_keys) + current_app.config['SECRET_KEY'])
    data['sign'] = generate_sign(sign_source_string)
    url = 'https://core.piastrix.com/bill/create'
    response = requests.post(
        url,
        json={**data},
        headers={'Content-Type': 'application/json'},
        timeout=TIMEOUT_SEC,
    )
    if not response.status_code == 200:
        raise Exception
    return response.json()


@app.route(
    '/place_order_via_invoice/<amount>/<currency>/<shop_order_id>/<shop_id>',
    methods=['GET', 'POST'])
def place_order_via_invoice(
        amount: str,
        currency: str,
        shop_order_id: uuid,
        shop_id: int,
        payway='payeer_rub'):
    """ Prepare data; post.request; render html based on response_data """

    data = locals()
    required_keys = ['amount', 'currency', 'payway', 'shop_id',
                     'shop_order_id']
    sign_source_string = (dict_values_concatenator(data, required_keys)
                          + current_app.config['SECRET_KEY'])
    data['sign'] = generate_sign(sign_source_string)
    url = 'https://core.piastrix.com/invoice/create'

    response = requests.post(
        url,
        json={**data},
        headers={'Content-Type': 'application/json'},
        timeout=TIMEOUT_SEC,
    )
    if not response.status_code == 200:
        raise Exception
    response_data = response.json()
    html_confirmation_form_data = {
        k: v for (k, v) in response_data['data']['data'].items()}
    return render_template("invoice_form.html", **html_confirmation_form_data)
