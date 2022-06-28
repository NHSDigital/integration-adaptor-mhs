import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.fail;
import static org.assertj.core.api.Assumptions.assumeThat;

import java.net.URI;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.DynamoDbException;
import software.amazon.awssdk.services.dynamodb.model.ScanRequest;
import software.amazon.awssdk.services.dynamodb.model.ScanResponse;
import util.EnvVarsUtil;

public class DynamoDbSmokeTest {

    private static final String DB_ENDPOINT_ENV_VAR = "MHS_DB_ENDPOINT_URL";
    private static final String CLOUD_REGION_DEFAULT_VALUE = "eu-west-2";
    private static final String CLOUD_REGION_ENV_VAR = "MHS_CLOUD_REGION";
    private static final String ACCESS_KEY_ID_ENV_VAR = "AWS_ACCESS_KEY_ID";
    private static final String ACCESS_KEY_ID_DEFAULT_VALUE = "test";
    private static final String ACCESS_KEY_ENV_VAR = "AWS_SECRET_ACCESS_KEY";
    private static final String ACCESS_KEY_DEFAULT_VALUE = "test";
    private static final String TABLE_NAME_ENV_VAR = "mhs_state";
    private static final String TABLE_NAME_DEFAULT_VALUE = "mhs_state";

    private static String uri;
    private static String cloudRegion;
    private static String accessKeyId;
    private static String accessKey;
    private static String tableName;

    @BeforeAll
    public static void setup() {
        Map<String, String> envVars = System.getenv();

        uri = envVars.getOrDefault(DB_ENDPOINT_ENV_VAR, null);
        uri = uri != null ? EnvVarsUtil.replaceContainerUri(uri, "http", "dynamodb") : null;

        cloudRegion = envVars.getOrDefault(CLOUD_REGION_ENV_VAR, CLOUD_REGION_DEFAULT_VALUE);
        accessKeyId = envVars.getOrDefault(ACCESS_KEY_ID_ENV_VAR, ACCESS_KEY_ID_DEFAULT_VALUE);
        accessKey = envVars.getOrDefault(ACCESS_KEY_ENV_VAR, ACCESS_KEY_DEFAULT_VALUE);
        tableName = envVars.getOrDefault(TABLE_NAME_ENV_VAR, TABLE_NAME_DEFAULT_VALUE);
    }

    @Test
    public void expect_dbUriIsDefined() {

        Optional<String> uriOptional = Optional.ofNullable(uri);

        assertThat(uriOptional.isPresent())
            .as("The environment variable " + DB_ENDPOINT_ENV_VAR + " must be defined")
            .isTrue();
    }


    @Test
    public void expect_DynamoDb_isAvailable() {

        Optional<String> uriOptional = Optional.ofNullable(uri);

        assumeThat(uriOptional.isPresent()).isTrue();

        try (DynamoDbClient client = DynamoDbClient.builder()
            .endpointOverride(URI.create(uri))
            .region(Region.of(cloudRegion))
            .credentialsProvider(StaticCredentialsProvider.create(
                AwsBasicCredentials.create(accessKeyId, accessKey)
            )).build()) {

            assertThat(tableExists(client))
                .as("Database should contain a table named: " + tableName)
                .isTrue();

            int count = countTableItems(client);

            assertThat(count >= 0)
                .as("Error reading from database")
                .isTrue();


        } catch (DynamoDbException e) {
            fail("Error connecting to database at: " + uri);
        }
    }

    private int countTableItems(DynamoDbClient client) throws DynamoDbException {

        ScanRequest request = ScanRequest.builder()
                .tableName(tableName)
                    .build();

        ScanResponse response = client.scan(request);

        return response.count();
    }

    private boolean tableExists(DynamoDbClient client) throws DynamoDbException {

        List<String> tableNames = client.listTables().tableNames();

        return tableNames.contains(tableName);
    }

}
