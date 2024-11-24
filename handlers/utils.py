import math
import logging
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def item_full_match(item):
    logger.info(f'Validting item: {item}')
    description = item.get('shortDescription', None)
    price = item.get('price', None)

    if not (description and price):
        logger.info('Required field(s) missing, item invalid')
        return None
    
    logger.info(f'Validating description: {description}')
    if re.fullmatch('^[\\w\\s\\-]+$', description) is None:
        logger.info('Invalid')
        return None
    logger.info('Valid')
    
    logger.info(f'Validating price: {price}')
    if re.fullmatch('^\\d+\\.\\d{2}$', price) is None:
        logger.info('Invalid')
        return None
    logger.info('Valid')
    
    logger.info('Item valid')
    return True

def validate_receipt(receipt):
    try:
        logger.info('validating receipt')
        retailer = receipt.get('retailer', None)
        purchase_date = receipt.get('purchaseDate', None)
        purchase_time = receipt.get('purchaseTime', None)
        items = receipt.get('items', None)
        total = receipt.get('total', None)

        if not (retailer and purchase_date and purchase_time and items and total):
            logger.info('Required field(s) missing, receipt invalid')
            return False
        
        logger.info(f'Validating retailer: {retailer}')
        if re.fullmatch('^[\\w\\s\\-&]+$', retailer) is None:
            logger.info('Invalid')
            return False
        logger.info('Valid')
        
        logger.info(f'Validating total: {total}')
        if re.fullmatch('^\\d+\\.\\d{2}$', total) is None:
            logger.info('Invalid')
            return False
        logger.info('Valid')
        
        for item in items:
            if item_full_match(item) is None:
                return False
            
        logger.info(f'Validating purchase time: {purchase_time}')
        if re.fullmatch('^([01]?[0-9]|2[0-3]):([0-5]?[0-9])$', purchase_time) is None:
            logger.info('Invalid')
            return False
        logger.info('Valid')
        
        logger.info(f'Validating purchase date: {purchase_date}')
        if re.fullmatch('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$', purchase_date) is None:
            logger.info('Invalid')
            return False
        logger.info('Valid')
    except Exception as error:
        logger.error(f'''Caught exception validating receipt, returning invalid. 
                     Error: {error}''')
        return False

    return True

def get_points_from_retailer(retailer):
    logger.info(f'Determining points from retailer name: {retailer}')

    points = 0

    if retailer is None:
        logger.info('Retailer not found on receipt, returning 0 points')
        return points
    
    try:
        for char in retailer:
            if char.isalnum():
                points += 1

        logger.info(f'Points calculated: {points}')
        return points
    except Exception as error:
        logger.error(f'Error determining points from alpha numeric count: {error}')
        return 0
    

def get_points_from_total(total):
    logger.info(f'Determining points from total: {total}')

    points = 0

    if total is None:
        logger.info('Total not found on receipt, returning 0 points')
        return points
    
    try:
        total = float(total)
        if math.ceil(total) == total:
            logger.info(f'Total is integer, adding 50 points')
            points += 50

        if total % 0.25 == 0:
            logger.info(f'Total is multiple of 0.25, adding 25 points')
            points += 25

        logger.info(f'Points calculated: {points}')
        return points
    except Exception as error:
        logger.error(f'Erro determining points from total: {error}')
        return 0


def get_points_from_items(items):
    logger.info(f'Determining points from items on receipt')

    points = 0
    
    try:
        if len(items) == 0:
            logger.info('Items not found on receipt, returning 0 points')
            return points

        points += 5*math.floor(len(items) / 2)
        
        for item in items:
            logger.info(f'Determining point from item: {item}')

            description = item.get('shortDescription', None)
            price = item.get('price', None)

            if description is None or price is None:
                logger.info(f'Description or price not found, continuing')
                continue

            price = float(price)

            if len(description.strip()) % 3 == 0:
                logger.info(f'''Trimmed description length is multiple of 3. 
                            Based on price: {price} adding: {math.ceil(price*0.2)} to points''')
                points += math.ceil(price * 0.2)

        logger.info(f'Points calculated: {points}')
        return points
    except Exception as error:
        logger.error(f'Error determining points from items: {error}')
        return 0

def get_points_from_purchase_date(date):
    logger.info(f'Determining points from date on receipt: {date}')

    points = 0

    if date is None:
        logger.info('Purchase date not found on receipt, returning 0 points')
        return points

    try:
        purchase_date = datetime.strptime(date, '%Y-%m-%d')

        if purchase_date.day % 2 != 0:
            logger.info(f'Purchase date is on odd day, adding 6 points')
            points += 6

        logger.info(f'Points calculated: {points}')
        return points
    except Exception as error:
        logger.error(f'Exception caught determining points from purchase date: {error}')
        return 0


def get_points_from_purchase_time(time):
    logger.info(f'Determining points from time on receipt: {time}')

    points = 0

    if time is None:
        logger.info('Purchase time not found on receipt, returning 0 points')
        return points
    
    try:
        (hour, minute) = time.split(':')

        hour_minute = 100*int(hour) + int(minute)
        
        logger.info(f'Split time string, hour*100 + minute: {hour_minute}')
        if hour_minute > 1400 and hour_minute < 1600:
            logger.info(f'Hour between 2 and 4, adding 10 points')
            points += 10

        logger.info(f'Points calculated: {points}')
        return points
    except Exception as error:
        logger.error(f'Exception caught determining points from purchase time: {error}')
        return 0


def determine_points(receipt):
    try:
        points = 0
        points += get_points_from_retailer(receipt.get('retailer', None))
        points += get_points_from_total(receipt.get('total', None))
        points += get_points_from_items(receipt.get('items', []))
        points += get_points_from_purchase_date(receipt.get('purchaseDate', None))
        points += get_points_from_purchase_time(receipt.get('purchaseTime', None))
    except Exception as error:
        logger.error(f'Error caught determining points for receipt: {error}')
        return 0

    logger.info(f'Total points calculated: {points}')
    return points
