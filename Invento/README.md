Models
1. Custom User Model

    Fields:
        email: (Primary key) Email address used as the login identifier.
        first_name: First name of the user.
        last_name: Last name of the user.
        id_no: Custom ID number for each user.
        password: User’s password.
    Authentication: Custom authentication with token-based login.

2. Item Model

    Fields:
        name: The name of the item.
        price: The price of the item.
        quantity: The current quantity of the item in stock.
        threshold: Minimum quantity to trigger low stock alerts.
        category: Foreign key linking to the Category model.
        creator: The user who created the item.

3. Category Model

    Fields:
        name: The name of the category.
        description: Description of the category.
        creator: The user who created the category.

4. Supplier Model

    Fields:
        name: The name of the supplier.
        contact_info: Contact details for the supplier.

5. Transaction Model

    Fields:
        item: The item involved in the transaction.
        transaction_type: Either sale or restock.
        quantity: The quantity of the item in the transaction.
        date: The date of the transaction.

ViewSets and Endpoints
CategoryViewSet

Handles CRUD operations for categories.

    GET /categories/: List all categories.
    POST /categories/: Create a new category.
    GET /categories/{id}/: Retrieve a category by ID.
    PUT /categories/{id}/: Update a category by ID.
    DELETE /categories/{id}/: Delete a category by ID.

ItemViewSet

Handles CRUD operations for items and supports filtering.

    GET /items/: List all items with filtering by category, price range, and low stock status. Supports pagination.
        Query Parameters:
            category: Filter by category ID.
            min_price & max_price: Filter by price range.
            low_stock: Filter items below the low stock threshold.
            ordering: Order results (e.g., by name, -price).
    POST /items/: Create a new item.
    GET /items/{id}/: Retrieve an item by ID.
    PUT /items/{id}/: Update an item by ID.
    DELETE /items/{id}/: Delete an item by ID.

InventoryChangeViewSet

Handles viewing changes to inventory.

    GET /inventory-changes/{item_id}/: View all changes in quantity for a specific item.

SupplierViewSet

CRUD operations for suppliers.

    GET /suppliers/: List all suppliers.
    POST /suppliers/: Create a new supplier.
    GET /suppliers/{id}/: Retrieve a supplier by ID.
    PUT /suppliers/{id}/: Update a supplier by ID.
    DELETE /suppliers/{id}/: Delete a supplier by ID.

InventoryReportViewSet

Provides a report on the total value of inventory.

    GET /inventory-reports/total_inventory_value/: Get the total value of all items in stock.

StockLevelReportViewSet

Provides a report on stock levels.

    GET /stock-level-reports/: List stock levels, optionally filtered by low stock.
        Query Parameters:
            low_stock: Filter items below the stock threshold (low_stock=true).

TransactionHistoryViewSet

Handles CRUD operations for transactions (sales/restocks).

    GET /transactions/: List all sales and restocks.
    POST /transactions/: Create a new transaction.
        Adjusts item quantity based on the transaction type (sale reduces quantity, restock increases quantity).
    GET /transactions/{id}/: Retrieve a transaction by ID.
    PUT /transactions/{id}/: Update a transaction by ID (adjusts item quantities accordingly).
    DELETE /transactions/{id}/: Delete a transaction (adjusts item quantities to undo the transaction).

Permissions

    IsOwnerOrReadOnly: Custom permission that ensures only the owner (creator) of an object can modify it, while others can view it.
        Apply this permission to models like Item, Category, and Transaction.
    IsAuthenticated: Ensures that only authenticated users can access the views.