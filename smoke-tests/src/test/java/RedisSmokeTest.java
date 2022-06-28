import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.fail;

import java.util.Map;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.exceptions.JedisConnectionException;

public class RedisSmokeTest {

    private static final String REDIS_HOST_ENV_VAR = "MHS_SDS_REDIS_CACHE_HOST";
    private static final String DEFAULT_REDIS_HOST = "localhost";
    private static final String DISABLE_TLS_ENV_VAR = "MHS_SDS_REDIS_DISABLE_TLS";
    private static final String REDIS_PORT_ENV_VAR = "REDIS_PORT";
    private static final String REDIS_PORT_DEFAULT_VALUE = "6379";

    private static JedisPool jedisPool;

    private static String dbLocation;

    @BeforeAll
    public static void setup() {

        Map<String, String> envVars = System.getenv();
        String redisPort = envVars.getOrDefault(REDIS_PORT_ENV_VAR, REDIS_PORT_DEFAULT_VALUE);
        String redisHost = envVars.getOrDefault(REDIS_HOST_ENV_VAR, DEFAULT_REDIS_HOST);

        redisHost = redisHost.equals("redis") ? "localhost" : redisHost;

        boolean useTSL = !envVars.get(DISABLE_TLS_ENV_VAR).equals("True");

        dbLocation = redisHost + ":" + redisPort;

        jedisPool = new JedisPool(DEFAULT_REDIS_HOST, Integer.parseInt(redisPort), useTSL);
    }

    @Test
    public void when_RedisPinged_Expect_Pong() {

        try(Jedis jedis = jedisPool.getResource()) {
            String response = jedis.ping();

            assertThat(response)
                .as("Redis connection check failed")
                .isEqualTo("PONG");
        } catch (JedisConnectionException e) {
            fail("Unable to connect to redis server at: " + dbLocation);
        }
    }

    @Test
    public void when_WrittenTo_Expect_ValueRead() {

        String testKey = "test key";
        String testValue = "test value";

        try(Jedis jedis = jedisPool.getResource()) {
            jedis.set(testKey, testValue);

            String response = jedis.get(testKey);

            assertThat(response)
                .as("Unexpected response value")
                .isEqualTo(testValue);

            jedis.del(testKey);

        } catch (JedisConnectionException e) {
            fail("Unable to connect to redis server at: " + dbLocation);
        }
    }


}
