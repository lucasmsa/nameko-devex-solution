# 🔖 Nameko-devex Back-end Test

<br>

## ⚙️ How to run

- Informations about how to run the project locally, as well as unit, smoke and performance tests are inside the `README-DevEnv.md`

## ✏️ Implemented Tasks

#### The files that were changed are on the `orders`, `products` and `gateway/gateway` folders, new routes, tests and extra functionalities were added to the application

- [x]  Enhance product service
    - Add a `Patch` method
    - Implement a products listing method
        - Add pagination and page size products listing
        - Add filtering options to the list method, filtering data by their respective titles
- [x]  Delete product rpc call
- [x]  (Extra) List orders rpc call
- [x]  Wire into [smoketest.sh](http://smoketest.sh/)
- [x]  (bonus) Wire into perf-test
- [x]  (bonus) Wire unit-test for this method

---

- [x]  Enhance order service
    - Classes were organized in a different manner, adding an `OrderServiceMixin` and `OrderDetailServiceMixin` to the `OrdersService`
    - Implemented a caching system using `lru_cache` for the
    - Adjusted the `_create_order` method, calling the `get` method instead of listing products
    - The same was done for the `_get_order` **method, calling only the `get` method, boosting the application's performance
- [x]  List orders rpc call
    - Pagination and per page query methods were implemented
- [x]  (Extra) Delete orders rpc call
- [x]  Wire into [smoketest.sh](http://smoketest.sh/)
- [x]  (bonus) Wire into perf-test
- [x]  (bonus) Wire unit-test for this method

---

### 🧪 Performance test questions

**Question 1**: Why is performance degrading as the test run longer?

- The most probable reason for performance degradation is because of the creation of orders and products everytime the performance test runs. This may cause resource exhaustion, by creating a large number of elements, the server-side resources (eg.: CPU, memory, database connections) may be exhausted, making the performance downgrade. Database is affected too in this case, as the size of the database grows, this may lead to slower query execution times if the database is not optimized or indexed correctly.

**Question 2**: How do you fix it?

- This problem can be fixed by cleaning up the test data, deleting orders and proucts that are no longer needed helps with the performance of the application, especially if the test is expected to run for a long time, helping to keep the database size manageable and maintaining a good performance even if the test runs for a long time
- [x]  **(bonus): Fix it**

 A new `Delete Order` test was added to the performance tests, making the tests maintain its performance even if it runs for a long time:
    
```
# 6. Delete Order
- url: /orders/${order_id}
    label: order-delete
    think-time: uniform(0s, 0s)
    method: DELETE

    assert:
    - contains:
    - 204
    subject: http-code
    not: false
```

- These methods are used by the `orders` and `products` services:

<p align='center'>
    <img src="https://i.imgur.com/CnT9Izw.png" alt="Insomnia Routes" style="height: 400px;"/>
</p>
