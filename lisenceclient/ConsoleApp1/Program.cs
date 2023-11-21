// See https://akusing System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Newtonsoft.Json.Linq;
Console.WriteLine("Enter your license key:");
string licenseKey = Console.ReadLine();

if (string.IsNullOrWhiteSpace(licenseKey))
{
    Console.WriteLine("License key cannot be empty.");
    return;
}

// Replace with your actual API endpoint
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
static string ExtractTokenFromJsonResponse(string jsonResponse)
{
    // Parse the JSON response
    JObject json = JObject.Parse(jsonResponse);

    // Extract the token property
    JToken tokenProperty = json["token"];

    // Convert the token property to a string
    return tokenProperty?.ToString();
}
// Create a JWT
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
