
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using RestSharp;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;

namespace trustid
{
    /// <summary>
    /// Interaction logic for login.xaml
    /// </summary>
    public partial class login : Window
    {
        public login()
        {
            InitializeComponent();
        }

        private void Grid_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.LeftButton == MouseButtonState.Pressed)
                DragMove();
        }

        public class LoginResponse
        {
            public string message { get; set; }
            public string resource_name { get; set; }

            public IDictionary<string, string> resource_obj { get; set; }
        }

        private async void btnLogin_Click(object sender, RoutedEventArgs e)
        {
            btnLogin.IsEnabled = false;
            btnLogin.Background = System.Windows.Media.Brushes.DarkGray;

            textBoxErrorMsg.Text = "";
            await Task.Delay(100);

            if (textBoxEmail.Text.Length == 0 || passwordBox1.Password.Length == 0)
            {
                textBoxErrorMsg.Text = "Please provide both email and password fields";
                btnLogin.IsEnabled = true;
                btnLogin.Background = new SolidColorBrush(Utilities.ConvertStringToColor("#0E71EB"));
                return;
            }

            try
            {
                var client = new RestClient("https://api.trustid-project.eu/backend/login/");
                client.Timeout = -1;
                var request = new RestRequest(Method.POST);
                request.AddHeader("Content-Type", "application/json");
                request.AddJsonBody(new
                {
                    email = textBoxEmail.Text,
                    password = passwordBox1.Password
                });
                IRestResponse restResponse = await client.ExecuteAsync(request);
                int status_code = (int)restResponse.StatusCode;

                if (status_code == ((int)HttpStatusCode.Created))
                {
                    Console.WriteLine("Success");
                    LoginResponse login_resp = JsonConvert.DeserializeObject<LoginResponse>(restResponse.Content);
                    string access_token = "";
                    string refresh_token = "";

                    if (login_resp.resource_obj.TryGetValue("access", out access_token))
                    {
                        Globals.jwt_access = access_token;
                    }
                    if (login_resp.resource_obj.TryGetValue("refresh", out refresh_token))
                    {
                        Globals.jwt_refresh = refresh_token;
                    }

                    // Decode JWT to find the role of the logged in user
                    var stream = access_token;
                    var handler = new JwtSecurityTokenHandler();
                    var jsonToken = handler.ReadToken(stream);
                    var tokenS = jsonToken as JwtSecurityToken;
                    var role = tokenS.Claims.First(claim => claim.Type == "role").Value;

                    var user_name = tokenS.Claims.First(claim => claim.Type == "name").Value;
                    var user_surname = tokenS.Claims.First(claim => claim.Type == "surname").Value;

                    Globals.user_name = user_name;
                    Globals.surname = user_surname;

                    if (role == "STUDENT")
                    {
                        Globals.role = "student";
                    }
                    else
                    {
                        Globals.role = "instructor";
                    }

                    textBoxErrorMsg.Foreground = Brushes.Green;
                    textBoxErrorMsg.Text = "Login success";

                    await Task.Delay(750);
                    Main newWindow = new Main();
                    newWindow.Show();
                    this.Close();
                }
                else if (status_code == ((int)HttpStatusCode.Unauthorized))
                {
                    Console.WriteLine("Unauthorized");
                    textBoxErrorMsg.Text = "Incorrect login credentials";
                }
                else if (status_code == ((int)HttpStatusCode.NotFound))
                {
                    Console.WriteLine("User not found");
                    textBoxErrorMsg.Text = "Incorrect login credentials";
                }
                else if (status_code == ((int)HttpStatusCode.InternalServerError))
                {
                    Console.WriteLine("Internal server error occurred. Try again later.");
                    textBoxErrorMsg.Text = "Internal server error occurred. Try again later.";
                }
            }
            catch (Exception exc)
            {
                Console.WriteLine("Application error occurred. Try again later: {0}", exc.Message);
                textBoxErrorMsg.Text = "Application error occurred. Try again later.";
            }

            btnLogin.IsEnabled = true;
            btnLogin.Background = new SolidColorBrush(Utilities.ConvertStringToColor("#0E71EB"));
        }
    }
}
