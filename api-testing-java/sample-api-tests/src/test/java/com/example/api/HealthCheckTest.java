package com.example.api;

import org.junit.jupiter.api.Test;
import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.empty;
import static org.hamcrest.Matchers.is;

public class HealthCheckTest extends BaseTest {

    @Test
    public void testHealthCheck() {
        given()
        .when()
            .get("/health")
        .then()
            .statusCode(200);
    }
}
