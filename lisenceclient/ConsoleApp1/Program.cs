// See https://akusing System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
Console.WriteLine("Enter your license key:");
string licenseKey = Console.ReadLine();

if (string.IsNullOrWhiteSpace(licenseKey))
{
    Console.WriteLine("License key cannot be empty.");
    return;
}

// Replace with your actual API endpoint
string apiUrl = "https://example.com/api/validate-license";

// Send the license key to the server
string response = await SendLicenseKey(apiUrl, licenseKey);

// Interpret the server response
Console.WriteLine("Server response:");
Console.WriteLine(response);
Console.WriteLine("validating lisence key");
var results = ValidateJwt(response, "your_secret_key");

if (results != null)
{
    Console.WriteLine("License key is valid.");
}
else
{
    Console.WriteLine("License key is invalid.");
}
// Create a JWT
static ClaimsPrincipal ValidateJwt(string jwt, string secretKey)
{
    var securityKey = new SymmetricSecurityKey(System.Text.Encoding.UTF8.GetBytes(secretKey));

    var tokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuer = true,
        ValidateAudience = true,
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = "expected_issuer", // Replace with the expected issuer
        ValidAudience = "expected_audience", // Replace with the expected audience
        IssuerSigningKey = securityKey
    };

    var handler = new JwtSecurityTokenHandler();
    try
    {
        SecurityToken securityToken;
        ClaimsPrincipal claimsPrincipal = handler.ValidateToken(jwt, tokenValidationParameters, out securityToken);

        // Additional validation logic can be added if needed

        return claimsPrincipal;
    }
    catch (Exception ex)
    {
        // Token validation failed
        Console.WriteLine($"Token validation error: {ex.Message}");
        return null;
    }
}
async Task<string> SendLicenseKey(string apiUrl, string licenseKey)
{
    using (var client = new HttpClient())
    {
        var content = new StringContent(licenseKey, Encoding.UTF8, "application/json");

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
