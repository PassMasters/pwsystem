// See https://akusing System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Newtonsoft.Json.Linq;
using Microsoft.Win32;
string registryKeyPath = "SOFTWARE\\YourCompany\\YourApp";
string valueName = "RandomNumber";

bool keyexsits = RandomNumberReg(registryKeyPath, valueName, out string randomNumber);
if (keyexsits != true)
{
    Console.WriteLine("Enter your license key:");
    string licenseKey = Console.ReadLine();

    if (string.IsNullOrWhiteSpace(licenseKey))
    {
        Console.WriteLine("License key cannot be empty.");
        return;
    }
    string apiUrl = "http://127.0.0.1:8000/key/TokenRequest/";

    // Send the license key to the server
    string response = await SendLicenseKey(apiUrl, licenseKey);
    string decodedToken = ExtractTokenFromJsonResponse(response);
    // Interpret the server response
    Console.WriteLine("Server response:");
    Console.WriteLine(response);
    Console.WriteLine("decoding:");
    DecodeJwt(decodedToken);
    Console.WriteLine("validating lisence key");
    var results = ValidateJwt(decodedToken, "OIDFJIODSFJIODSFJIU(WFHOISDF903248uweriy87345ureiyrtb965258752475201258525475sduri6838ejmfiuvmknmeujdjedjdjjdjdjdjd)");

    if (results != null)
    {
        Console.WriteLine("License key is valid.");
    }
    else
    {
        Console.WriteLine("License key is invalid.");
    }
}
else
{
    Console.WriteLine("SystemManagement");
    Console.WriteLine("press 1 for Deactivate");
    Console.WriteLine("press 2 for device registration");
    Console.WriteLine("press 3 to download your passwords from server");
    Console.WriteLine("press 4 to chnage lisence key");
    Console.WriteLine("press 5 to exit");
    Console.WriteLine("press 6 to uninstall app");
    int option = Convert.ToInt32(Console.ReadLine());
    switch (option)
    {
        case 1:
            Console.WriteLine("Enter your license key:");
            string licenseKey = Console.ReadLine();
            await RemoveLisence(licenseKey);
            break;
        case 2:
            break;
        case 3:
            break;
        case 4:
            break;
        case 5:
            break;
        default:
            break;
    }
}


 async  Task RemoveLisence(string key)
{
    string apiUrl = "http://127.0.0.1:8000/key/Deactivate/";
    await SendLicenseKey(apiUrl, key);
}

// Replace with your actual API endpoint

static string ExtractTokenFromJsonResponse(string jsonResponse)
{
    // Parse the JSON response
    JObject json = JObject.Parse(jsonResponse);

    // Extract the token property
    JToken tokenProperty = json["token"];

    // Convert the token property to a string
    return tokenProperty?.ToString();
}
//validate jwt
static ClaimsPrincipal ValidateJwt(string jwt, string secretKey)
{
    var securityKey = new SymmetricSecurityKey(System.Text.Encoding.UTF8.GetBytes(secretKey));

    var tokenValidationParameters = new TokenValidationParameters
    {

        ValidateIssuer = false, // Set to true if you want to validate the issuer
        ValidateAudience = false, // Set to true if you want to validate the audience
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = securityKey,
        ClockSkew = TimeSpan.Zero, // Set to zero to validate exp claims without allowing for clock skew
        RequireSignedTokens = true, // Requires signed tokens
        RequireExpirationTime = true,
        ValidAlgorithms = new[] { SecurityAlgorithms.HmacSha256 },
    };

    var handler = new JwtSecurityTokenHandler();
    try
    {
        SecurityToken securityToken;
        ClaimsPrincipal claimsPrincipal = handler.ValidateToken(jwt, tokenValidationParameters, out securityToken);

        // Additional validation logic can be added if needed
        int randomNumber = int.Parse(claimsPrincipal.FindFirst("random_number")?.Value);
        string data = randomNumber.ToString();
        StoreRandomNumberInRegistry(data, "rand");
        Console.WriteLine("JWT is valid!");
        return claimsPrincipal;
        
    }
    catch (Exception ex)
    {
        // Token validation failed
        Console.WriteLine($"Token validation error: {ex.Message}");
        return null;
    }
}
static void DecodeJwt(string jwt)
{
    var handler = new JwtSecurityTokenHandler();

    try
    {
        var jsonToken = handler.ReadToken(jwt) as JwtSecurityToken;

        if (jsonToken != null)
        {
            // Access token claims
            foreach (var claim in jsonToken.Claims)
            {
                Console.WriteLine($"{claim.Type}: {claim.Value}");
            }
        }
        else
        {
            Console.WriteLine("Invalid token format");
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Token decoding error: {ex.Message}");
    }
}
async Task<string> SendLicenseKey(string apiUrl, string licenseKey)
{
    using (var client = new HttpClient())
    {
        var content = new StringContent($"key={licenseKey}", Encoding.UTF8, "application/x-www-form-urlencoded");

        var response = await client.PostAsync(apiUrl, content);

        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadAsStringAsync();
        }
        else
        {
            return $"Error: {response.StatusCode}";
        }
    }
}
static void StoreRandomNumberInRegistry(string data, string keyname)
{
    // Specify the registry key path (you can customize this)
    string registryKeyPath = "SOFTWARE\\Passmasters\\PWsystem";

    // Open or create the registry key
    using (var registryKey = Registry.CurrentUser.CreateSubKey(registryKeyPath))
    {
        // Store the random number in the registry
        registryKey?.SetValue(keyname, data);
    }
}
static bool RandomNumberReg(string keyPath, string valueName, out string randomNumber)
{
    // Open the registry key for reading
    using (var registryKey = Registry.CurrentUser.OpenSubKey(keyPath))
    {
        // Check if the registry key exists
        if (registryKey != null)
        {
            // Check if the value exists in the registry
            if (registryKey.GetValue(valueName) is string value)
            {
                // The value exists, assign it to 'randomNumber' and return true
                randomNumber = value;
                return true;
            }
        }
    }

    // The value does not exist or there was an error, assign a default value to 'randomNumber' and return false
    randomNumber =" 0";
    return false;
}
