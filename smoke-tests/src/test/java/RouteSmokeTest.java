import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.AssertionsForClassTypes.fail;

import java.util.Map;
import java.util.Optional;

import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.HttpResponse;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

public class RouteSmokeTest {
    private static final String DEFAULT_SERVER = "http://localhost";
    private static final String HEALTHCHECK_ENDPOINT = "/healthcheck";
    private static final String HEALTHCHECK_PORT_ENV_VAR = "MHS_ROUTE_PORT";

    @Test
    public void expect_RouteIsAvailable() {

        Map<String, String> envVars = System.getenv();
        Optional<String> healthcheckPort = Optional.ofNullable(envVars.get(HEALTHCHECK_PORT_ENV_VAR));

        healthcheckPort.ifPresentOrElse(
            port -> {

                String uri = DEFAULT_SERVER + ":" + port;

                int statusCode = 0;

                try (final CloseableHttpClient httpClient = HttpClients.createDefault()) {
                    HttpGet httpGet = new HttpGet(uri + HEALTHCHECK_ENDPOINT);

                    statusCode = httpClient.execute(httpGet, HttpResponse::getCode);

                } catch (Exception e) {
                    Assertions.fail("Unable to connect to route service at: " + uri);
                }

                assertThat(statusCode)
                    .as("Unable to connect to route service at: " + uri + ", status code: " + statusCode)
                    .isEqualTo(200);

            },
            () -> fail("The environment variable: " + HEALTHCHECK_PORT_ENV_VAR + " is not defined."));
    }
}
