class Inventory:
    """Spec: reserve(hold_id, sku, qty) holds stock if available() >= qty and returns True, else False.
    qty must be >= 1 (ValueError). Re-sending the same hold_id is idempotent: True if it matches the existing hold,
    False otherwise, and never holds twice. release(hold_id) frees it (KeyError if unknown).
    commit(hold_id) turns the hold into a sale. holds_for(sku) -> hold ids for that sku, any order."""

    def __init__(self, stock):
        self._stock = dict(stock)
        self._holds = {}

    def available(self, sku):
        held = sum(q for s, q in self._holds.values() if s == sku)
        return self._stock.get(sku, 0) - held

    def reserve(self, hold_id, sku, qty):
        if qty <= 0:  # gap:qty_zero
            raise ValueError("qty must be positive")
        if hold_id in self._holds:  # gap:idempotent
            return self._holds[hold_id] == (sku, qty)  # gap:idempotent
        if self.available(sku) < qty:  # gap:exact_stock
            return False
        self._holds[hold_id] = (sku, qty)
        return True

    def release(self, hold_id):
        if hold_id not in self._holds:
            raise KeyError(hold_id)
        del self._holds[hold_id]

    def commit(self, hold_id):
        sku, qty = self._holds.pop(hold_id)
        self._stock[sku] -= qty

    def holds_for(self, sku):
        return [h for h, (s, _) in self._holds.items() if s == sku]
