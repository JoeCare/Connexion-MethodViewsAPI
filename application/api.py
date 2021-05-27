from flask import jsonify, request
from flask.views import MethodView
from application.models import db, mm, Dish, MenuCard


class DishesView(MethodView):
    def get(self, pk):
        logger.info('LOGGGETTTT!!!!!!!!!')
        if pk:
            dish = Dish.query.filter(Dish.id == pk).one_or_none()
            if dish:
                logger.debug('logggerr!!!!!!!!!')
                return jsonify(200, dish.serialize())
            else:
                logger.debug('logggerr!!!!!!!!!')
                return jsonify(404, 'Not found')
        else:
            dishes = Dish.query.all()
            if dishes:
                logger.warning('logggerr!!!!!!!!!')
                print('printerrr!!!!!!!!!')
                return jsonify(200, [dish.serialize() for dish in dishes])
            else:
                return jsonify(404, 'No records found')

    def post(self):

        body = request.get_json()
        menus = body.get('cards', None)
        if menus:
            for ids in menus:
                print(1, menus, ids)
                menus.insert(menus.index(ids), MenuCard.query.get(ids))
                print(2, menus, ids)
                menus.remove(ids)
                print(3, menus, ids)
            body['cards'] = [
                menu for menu in menus if isinstance(menu, MenuCard)]
            print(type(menus[0]), menus, body)
            new_dish = Dish(**body)
            db.session.add(new_dish)
            db.session.commit()
            return jsonify(201, 'Created')
        # new_dish = Dish(**body)   should be around 35th line
        # if new_dish.is_unique(new_dish.name):
        #     db.session.add(new_dish)
        #     db.session.commit()
        #     return jsonify(201, 'Created', new_dish.serialize(), 'from', body)
        # else:
        #     return jsonify(400, 'Name already in database')

    def put(self, pk):
        body = request.get_json()
        menus = body.get('cards', None)
        old_dish = Dish.query.get(pk)
        if old_dish:
            pass
        if menus:
            for ids in menus:
                print(1, menus, ids)
                menus.insert(menus.index(ids), MenuCard.query.get(ids))
                print(2, menus, ids)
                menus.remove(ids)
                print(3, menus, ids)
            body['cards'] = [
                menu for menu in menus if isinstance(menu, MenuCard)]
            print(type(menus[0]), menus, body)
            new_dish = Dish(**body)
            db.session.add(new_dish)
            db.session.commit()
            return jsonify(201, 'Created')

    def delete(self, pk):
        pass


class CardsView(MethodView):

    def get(self, pk):

        if pk:
            card = MenuCard.query.filter_by(id=pk).one_or_none()
            if card:
                return jsonify(200, card.serialize())
            else:
                return jsonify(404, 'Not found')
        else:
            cards = MenuCard.query.all()
            if cards:
                return jsonify(200, [card.serialize() for card in cards])
            else:
                return jsonify(404, 'No records found')

    # if menus:
    #     schemas = menus_schema.dump(menus)
    #     return jsonify(200, schemas)
    # else:
    #     return jsonify(404, "Not found any records")

    # a tak wyglada chyba wersja jsonowa bez marshmallow : o
    # output = []
    #
    # for menu in menus:
    #     menu_data = {}
    #     menu_data['id'] = user.public_id
    #     menu_data['name'] = user.name
    #     menu_data['description'] = user.password
    #     menu_data['vegetarian_card'] = user.admin
    #     menu_data['public_card'] = user.admin
    #     menu_data['dishes'] = user.admin
    #     menu_data['created_on'] = user.admin
    #     menu_data['vegetarian_card'] = user.admin
    #     output.append(menu_data)
    def post(self):
        body = request.get_json()
        dishes = body.get('dishes', None)
        if dishes:
            for ids in dishes:
                print(1, dishes, ids)
                dishes.insert(dishes.index(ids), Dish.query.get(ids))
                print(2, dishes, ids)
                dishes.remove(ids)
                print(3, dishes, ids)
            body['dishes'] = [dish for dish in dishes if isinstance(dish, Dish)]
            print(type(dishes[0]), dishes, body)
            new_card = MenuCard(**body)
            db.session.add(new_card)
            db.session.commit()
            return jsonify(201, 'Created')

        #     if new_card.is_unique(new_card.name):
        #         # db.session.add(new_card)
        #         # db.session.commit()
        #         return jsonify(201, 'Created', new_card.serialize())
        #     else:
        #         return jsonify(400, 'Name already in database')
        # else:
        #     new_card = MenuCard(**body)
        #     if new_card.is_unique(new_card.name):
        #         return jsonify('nie podales dishes?')
        #     else:
        #         return jsonify(400, 'Name already in database')

    def put(self, pk):

        body = request.get_json()
        dishes = body.get('dishes', None)
        if dishes:
            for ids in dishes:
                print(1, dishes, ids)
                dishes.insert(dishes.index(ids), Dish.query.get(ids))
                print(2, dishes, ids)
                dishes.remove(ids)
                print(3, dishes, ids)
            body['dishes'] = [dish for dish in dishes if isinstance(dish, Dish)]
            print(type(dishes[0]), dishes, body)
            new_card = MenuCard(**body)
            db.session.add(new_card)
            db.session.commit()
            return jsonify(201, 'Created')

    def delete(self, pk):
        pass


cards_view = CardsView.as_view('cards-api')
dishes_view = DishesView.as_view('dishes-api')
