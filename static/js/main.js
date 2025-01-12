// Stock update function with optimistic UI update
function updateStock(itemId, change) {
// 画像プレビュー機能
function previewImage(input) {
    const preview = document.getElementById('imagePreview');
    const previewImg = preview.querySelector('img');
    
    if (input.value) {
        previewImg.src = input.value;
        preview.style.display = 'block';
        previewImg.onerror = function() {
            preview.style.display = 'none';
        };
    } else {
        preview.style.display = 'none';
    }
}
    const stockElement = document.querySelector(`#item-${itemId} .stock-value`);
    const stockContainer = stockElement?.closest('.item-stock');
    if (!stockElement || !stockContainer) return;

    const currentStock = parseInt(stockElement.textContent);
    const minimumStock = parseInt(stockContainer.dataset.minimumStock || '0');
    const newStock = currentStock + change;

    // Update minus button state
    const minusButton = document.querySelector(`#item-${itemId} .btn-stock:first-child`);
    if (minusButton) {
        minusButton.disabled = newStock <= 0;
    }

    // Optimistic UI update
    stockElement.textContent = newStock;
    updateStockWarning(stockContainer, newStock, minimumStock);

    // Async backend update
    fetch(`/item/${itemId}/update_stock`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ change: change })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            // Rollback UI if backend update fails
            stockElement.textContent = currentStock;
            updateStockWarning(stockContainer, currentStock, minimumStock);
            alert('在庫の更新に失敗しました');
        }
    })
    .catch(error => {
        console.error('Error updating stock:', error);
        // Rollback UI on error
        stockElement.textContent = currentStock;
        updateStockWarning(stockContainer, currentStock, minimumStock);
        alert('在庫の更新中にエラーが発生しました');
    });
}

// Helper function to update stock warning display
function updateStockWarning(container, stock, minimumStock) {
    if (stock < minimumStock) {
        container.classList.add('low-stock');
        const neededItems = minimumStock - stock;
        container.setAttribute('data-restock-message', `あと${neededItems}個必要です`);
    } else {
        container.classList.remove('low-stock');
        container.removeAttribute('data-restock-message');
    }
}

// Delete item function
function deleteItem(itemId) {
    if (confirm('本当にこのアイテムを削除しますか？')) {
        fetch(`/item/${itemId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const itemElement = document.getElementById(`item-${itemId}`);
                if (itemElement) {
                    itemElement.remove();
                }
            } else {
                alert('アイテムの削除中にエラーが発生しました');
            }
        })
        .catch(error => {
            console.error('Error deleting item:', error);
            alert('アイテムの削除中にエラーが発生しました');
        });
    }
}

// フラッシュメッセージの初期化と自動非表示の設定
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        // 3秒後にフェードアウトを開始
        setTimeout(() => {
            message.classList.add('fade-out');
            // フェードアウト完了後に要素を削除
            setTimeout(() => {
                if (message && message.parentElement) {
                    message.remove();
                }
            }, 500); // CSSのアニメーション時間と合わせる
        }, 3000);

        // クリックイベントでも即座に削除
        const closeButton = message.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                message.remove();
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // フラッシュメッセージの初期化を呼び出し
    initializeFlashMessages();

    // Initialize Sortable
    let sortableInstance = null;
    const sortableList = document.getElementById('sortableList');
    const toggleMoveButton = document.getElementById('toggleMoveMode');
    let moveMode = false;
    
    function toggleMoveMode() {
        moveMode = !moveMode;
        if (moveMode) {
            // Enable move mode
            sortableList.classList.add('move-mode');
            toggleMoveButton.classList.remove('btn-light');
            toggleMoveButton.classList.add('btn-outline-dark');
            
            sortableInstance = new Sortable(sortableList, {
                animation: 150,
                ghostClass: 'sortable-ghost',
                dragClass: 'sortable-drag',
                chosenClass: 'sortable-chosen',
                filter: '.non-sortable',
                onStart: function() {
                    toggleMoveButton.textContent = 'Done';
                },
                onEnd: function(evt) {
                    const itemId = evt.item.id.split('-')[1];
                    const newIndex = evt.newIndex;
                    
                    fetch(`/item/${itemId}/reorder`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            new_index: newIndex
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (!data.success) {
                            console.error('Reorder failed:', data.error);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                }
            });
        } else {
            // Disable move mode
            sortableList.classList.remove('move-mode');
            toggleMoveButton.textContent = 'Move';
            toggleMoveButton.classList.remove('btn-outline-dark');
            toggleMoveButton.classList.add('btn-light');
            
            if (sortableInstance) {
                sortableInstance.destroy();
                sortableInstance = null;
            }
        }
    }
    
    // Initialize any Bootstrap components
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize dropdowns
    const dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl);
    });

    // Low stock filter functionality
    const toggleLowStockButton = document.getElementById('toggleLowStock');
    let showingLowStockOnly = false;

    if (toggleLowStockButton) {
        const noLowStockMessage = document.createElement('div');
        noLowStockMessage.className = 'alert alert-info mt-3';
        noLowStockMessage.id = 'noLowStockMessage';
        noLowStockMessage.style.display = 'none';
        noLowStockMessage.textContent = '買い物が必要な商品はありませんでした';
        document.querySelector('.inventory-list').after(noLowStockMessage);

        toggleLowStockButton.addEventListener('click', function() {
            showingLowStockOnly = !showingLowStockOnly;
            this.classList.toggle('btn-primary');
            this.classList.toggle('btn-outline-primary');
            
            const items = document.querySelectorAll('.inventory-row:not(.non-sortable)');
            let hasLowStockItems = false;

            items.forEach(item => {
                const stockContainer = item.querySelector('.item-stock');
                if (showingLowStockOnly) {
                    const isLowStock = stockContainer.classList.contains('low-stock');
                    item.style.display = isLowStock ? '' : 'none';
                    if (isLowStock) hasLowStockItems = true;
                } else {
                    item.style.display = '';
                }
            });

            // Show/hide no low stock message
            noLowStockMessage.style.display = (showingLowStockOnly && !hasLowStockItems) ? '' : 'none';
        });
    }

    // Attach move mode toggle event
    if (toggleMoveButton) {
        toggleMoveButton.addEventListener('click', toggleMoveMode);
    }

    // Delete item functionality
    document.querySelectorAll('.delete-item').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            deleteItem(itemId);
        });
    });

    // Stock level indicators
    document.querySelectorAll('.stock-level').forEach(function(element) {
        const stockLevel = parseInt(element.textContent);
        if (stockLevel <= 0) {
            element.classList.add('out-of-stock');
        }
    });

    // Form validation
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Category filtering
    const categoryButtons = document.querySelectorAll('.category-filter');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.dataset.category;
            const items = document.querySelectorAll('.inventory-item');
            
            items.forEach(item => {
                if (category === 'all' || item.dataset.category === category) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });

            // Update active state of filter buttons
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Search functionality
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const items = document.querySelectorAll('.inventory-item');
            
            items.forEach(item => {
                const itemName = item.querySelector('h3').textContent.toLowerCase();
                if (itemName.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
});

// Make updateStock globally accessible
window.updateStock = updateStock;
