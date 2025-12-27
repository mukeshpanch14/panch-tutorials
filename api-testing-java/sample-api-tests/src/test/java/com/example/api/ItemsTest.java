package com.example.api;

import com.example.api.models.Item;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.Test;
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.notNullValue;

public class ItemsTest extends BaseTest {

    @Test
    public void testCreateItem() {
        Item newItem = new Item("Notebook", "A place for ideas");

        given()
            .contentType(ContentType.JSON)
            .body(newItem)
        .when()
            .post("/items")
        .then()
            .statusCode(200)
            .body("name", equalTo("Notebook"))
            .body("item_id", notNullValue());
    }

    @Test
    public void testGetItem() {
        String testId = "test_item_123";

        // Note: The mock API returns the ID passed in the URL
        given()
        .when()
            .get("/items/" + testId)
        .then()
            .statusCode(200)
            .body("item_id", equalTo(testId));
    }

    @Test
    public void testUpdateItem() {
        String testId = "test_item_123";
        Item updatedItem = new Item("Macbook", "Expensive notebook");

        given()
            .contentType(ContentType.JSON)
            .body(updatedItem)
        .when()
            .put("/items/" + testId)
        .then()
            .statusCode(200)
            .body("name", equalTo("Macbook"))
            .body("item_id", equalTo(testId));
    }
}
