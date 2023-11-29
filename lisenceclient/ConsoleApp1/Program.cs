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
using System.IO.Compression;
using System.Diagnostics;
string registryKeyPath = "SOFTWARE\\Passmasters\\PWsystem";
string valueName = "rand";

bool keyexsits = RandomNumberReg(registryKeyPath, valueName, out string _);
if (keyexsits != true)
{
    Console.WriteLine("Enter your license key:");
    string licenseKey = Console.ReadLine();

    if (string.IsNullOrWhiteSpace(licenseKey))
    {
        Console.WriteLine("License key cannot be empty.");
        return;
    }
    string apiUrl = "https://munchypwsystem-ruby.vercel.app/key/TokenRequest/";

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
        Console.WriteLine("Begining Setup of local Password Manager Instance");
        string currentDirectory = AppDomain.CurrentDomain.BaseDirectory;
        string JSON = await MakeGetRequest("https://munchypwsystem-ruby.vercel.app/Version");
        bool configdownload = await DownloadFile("https://pacakagecdnpw.blob.core.windows.net/ooooooo/settings.py", currentDirectory);
        JObject jObject = JObject.Parse(JSON);
        string PackageURL = jObject["URL"].ToString();
        string Version = jObject["Version"].ToString();
        if (configdownload == true)
        {
            Console.WriteLine("Configuration data Downloaded");
            Console.WriteLine("Downlaoding Version: " + Version);
            bool downlaodstatus = await DownloadFile(PackageURL, currentDirectory);
            if (downlaodstatus == true)
            {
                Console.WriteLine("Package Downloaded");
                Console.WriteLine("Extracting Package");
                string zipPath = Path.Combine(currentDirectory, "package.zip");
                string extractPath = Path.Combine(currentDirectory, "package");
                try
                {
                    ZipFile.ExtractToDirectory(zipPath, extractPath);
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error extracting zip file: " + ex.Message);
                }

                try
                {
                    File.Delete(zipPath);
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error deleting zip file: " + ex.Message);
                }
                Console.WriteLine("Package Extracted");
                Console.WriteLine("Starting Setup");
                ProcessStartInfo psi = new ProcessStartInfo();
                psi.FileName = "pip";

                //join the arguments with a space, this allows you to set "app.apk" to a variable
                psi.Arguments = String.Join("install", " ","-r",  " ", "requirements.txt");
                psi.WorkingDirectory = extractPath;
                //leave it to the application, not the OS to launch the file
                psi.UseShellExecute = false;

                //choose to not create a window
                psi.CreateNoWindow = true;

                //set the window's style to 'hidden'
                psi.WindowStyle = ProcessWindowStyle.Hidden;

                var proc = new Process();
                proc.StartInfo = psi;
                proc.Start();
                proc.WaitForExit();
            //movefile

            }
            else
            {
                Console.WriteLine("Package Download Failed");
            }
        }
        else
        {
            Console.WriteLine("Config Download Failed");

        }
    }
    else
    {
        Console.WriteLine("License key is invalid.");
    }
}
else
{
    Console.WriteLine("System Management");
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
    string apiUrl = "https://munchypwsystem-ruby.vercel.app/key/Deactivate/";
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
        string data = claimsPrincipal.FindFirst("random_number")?.Value;
       
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
static async Task<string> MakeGetRequest(string apiUrl)
{
    using (HttpClient client = new HttpClient())
    {
        // Send GET request
        HttpResponseMessage response = await client.GetAsync(apiUrl);

        // Check if the request was successful
        if (response.IsSuccessStatusCode)
        {
            // Read and return the response content as a string
            return await response.Content.ReadAsStringAsync();
        }
        else
        {
            // Handle the error (throw an exception, return an error message, etc.)
            Console.WriteLine($"Error: {response.StatusCode} - {response.ReasonPhrase}");
            return string.Empty;
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
static async Task<bool> DownloadFile(string fileUrl, string localFilePath)
{
    try
    {
        using (HttpClient client = new HttpClient())
        {
            // Send GET request and get the response
            HttpResponseMessage response = await client.GetAsync(fileUrl);

            // Check if the request was successful
            if (response.IsSuccessStatusCode)
            {
                // Read the response stream and save it to a local file
                using (var fileStream = await response.Content.ReadAsStreamAsync())
                using (var file = System.IO.File.Create(localFilePath))
                {
                    await fileStream.CopyToAsync(file);
                }

                return true; // Download successful
            }
            else
            {
                Console.WriteLine($"Error: {response.StatusCode} - {response.ReasonPhrase}");
                return false; // Download failed
            }
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Exception: {ex.Message}");
        return false; // Download failed
    }
}
