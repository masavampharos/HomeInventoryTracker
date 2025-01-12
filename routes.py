from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from app import app, db
from models import Item, ConsumptionLog
from forms import ItemForm, ConsumptionForm
from flask import render_template, redirect, url_for, flash, request
from app import app, db
from models import Item, ConsumptionLog
from forms import ItemForm, ConsumptionForm
from datetime import datetime

@app.route('/')
def index():
    items = Item.query.order_by(Item.order_index).all()
    form = ItemForm()
    consumption_form = ConsumptionForm()
    items_to_restock = Item.query.filter(Item.current_stock <= Item.minimum_stock).all()
    return render_template('inventory.html', items=items, form=form, consumption_form=consumption_form, restock_items=items_to_restock)

@app.route('/item/add', methods=['GET', 'POST'])
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            name=form.name.data,
            current_stock=form.current_stock.data,
            minimum_stock=form.minimum_stock.data,
            image_url=form.image_url.data
        )
        db.session.add(item)
        db.session.commit()
        flash('アイテムを追加しました！', 'success')
        return redirect(url_for('index'))
    
    # GETリクエストの場合は空のフォームを表示
    items = Item.query.order_by(Item.order_index).all()
    consumption_form = ConsumptionForm()
    return render_template('inventory.html', form=form, items=items, consumption_form=consumption_form)

@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm()
    items = Item.query.order_by(Item.order_index).all()
    
    if form.validate_on_submit():
        try:
            item.name = form.name.data
            item.current_stock = form.current_stock.data
            item.minimum_stock = form.minimum_stock.data
            item.image_url = form.image_url.data
            item.last_updated = datetime.utcnow()
            
            db.session.commit()
            flash('Item updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating item {item_id}: {str(e)}")
            flash('Error updating item. Please try again.', 'error')
    
    # フォームにアイテムの現在の値を設定
    form.name.data = item.name
    form.current_stock.data = item.current_stock
    form.minimum_stock.data = item.minimum_stock
    form.image_url.data = item.image_url
    
    return render_template('inventory.html', form=form, items=items, item=item)

@app.route('/item/<int:item_id>/delete')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/item/<int:item_id>/consume', methods=['POST'])
def consume_item(item_id):
    item = Item.query.get_or_404(item_id)
    form = ConsumptionForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        if quantity <= item.current_stock:
            item.current_stock -= quantity
            log = ConsumptionLog(item_id=item.id, quantity=quantity)
            db.session.add(log)
            db.session.commit()
            flash('Consumption logged successfully!', 'success')
        else:
            flash('Not enough stock!', 'error')
    return redirect(url_for('index'))

@app.route('/item/<int:item_id>/update_stock', methods=['POST'])
def update_stock(item_id):
    item = Item.query.get_or_404(item_id)
    try:
        data = request.get_json()
        change = data.get('change', 0)
        new_stock = item.current_stock + change
        
        if new_stock >= 0:
            item.current_stock = new_stock
            item.last_updated = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'success': True,
                'new_stock': item.current_stock,
                'minimum_stock': item.minimum_stock
            })
        return jsonify({
            'success': False,
            'error': '在庫数は0未満にできません'
        }), 400
    except ValueError:
        return jsonify({
            'success': False,
            'error': '不正な値です'
        }), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating stock for item {item_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': '在庫の更新中にエラーが発生しました'
        }), 500
@app.route('/restock-list')
def restock_list():
    items_to_restock = Item.query.filter(Item.current_stock <= Item.minimum_stock).all()
    return render_template('inventory.html', restock_items=items_to_restock)


@app.route('/item/<int:item_id>/reorder', methods=['POST'])
def reorder_item(item_id):
    try:
        data = request.get_json()
        new_index = data.get('new_index')
        
        if new_index is None:
            return jsonify({'success': False, 'error': 'New index is required'}), 400
            
        # Update all items' order
        items = Item.query.order_by(Item.order_index).all()
        item_to_move = next((item for item in items if item.id == item_id), None)
        
        if not item_to_move:
            return jsonify({'success': False, 'error': 'Item not found'}), 404
            
        # Remove item from current position
        items.remove(item_to_move)
        # Insert item at new position
        items.insert(new_index, item_to_move)
        
        # Update order_index for all items
        for i, item in enumerate(items):
            item.order_index = i
            
        db.session.commit()
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500