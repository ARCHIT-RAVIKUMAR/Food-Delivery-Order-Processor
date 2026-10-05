# Obstacle Log

1. **Unknown menu item crashed the program.** Looking up "Sushi" in the menu dictionary gave a KeyError. I added `check_order()` which checks `name in menu` first and skips the order with a message.

2. **Empty orders gave a bill of Rs 40.** An empty order still got the delivery charge added, so it looked like a real order. I now check `len(items) == 0` and reject it before calculating anything.

3. **Quantity of 0.** An order with 0 burgers passed the menu check but made no sense. I added a check that the quantity must be more than 0.

4. **Finding the highest order when there are no valid orders.** Comparing against an empty list would fail, so I start `highest` as `None` and check for that before printing.

5. **Counting rejected orders in revenue.** I kept valid and invalid orders in two separate lists so only valid ones count toward revenue.
