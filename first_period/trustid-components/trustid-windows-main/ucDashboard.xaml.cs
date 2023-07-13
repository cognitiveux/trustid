using Newtonsoft.Json;
using RestSharp;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace trustid
{
    /// <summary>
    /// Interaction logic for ucDashboard.xaml
    /// </summary>
    public partial class ucDashboard : UserControl
    {
        public ucDashboard()
        {
            InitializeComponent();

            if (Globals.role == "student")
            {
                listExams();
            }
            else
            {
                listInstructorExams();
            }
        }

        public class StudentListExamResponse
        {
            public string message { get; set; }
            public string resource_name { get; set; }
            public IList<IDictionary<string, string>> resource_array { get; set; }
        }

        public class InstructorListExamResponse
        {
            public string message { get; set; }
            public string resource_name { get; set; }
            public IList<IDictionary<string, dynamic>> resource_array { get; set; }
        }

        public class UpdateExamConditionResponse
        {
            public string message { get; set; }
            public string resource_name { get; set; }
        }

        private async void listInstructorExams()
        {
            try
            {
                var client = new RestClient("https://api.trustid-project.eu/backend/instructor/list_exam/");
                client.Timeout = -1;
                var request = new RestRequest(Method.GET);
                request.AddHeader("Content-Type", "application/json");
                request.AddHeader("Authorization", "Bearer " + Globals.jwt_access);

                IRestResponse restResponse = await client.ExecuteAsync(request);
                int status_code = (int)restResponse.StatusCode;

                if (status_code == ((int)HttpStatusCode.OK))
                {
                    Console.WriteLine("Success");
                    InstructorListExamResponse listexam_resp = JsonConvert.DeserializeObject<InstructorListExamResponse>(restResponse.Content);
                    Console.WriteLine("listexam resource_name: " + listexam_resp.resource_name);
                    Console.WriteLine("listexam resource_array: " + listexam_resp.resource_array);

                    if (listexam_resp.resource_array.Count > 0)
                    {
                        dynamic exam_id = "";
                        dynamic exam_status = "";
                        dynamic scheduled_date = "";
                        dynamic exam_name = "";
                        dynamic enrolled_students;

                        if (listexam_resp.resource_array[0].TryGetValue("name", out exam_name))
                        {
                            examName.Text = examName.Text + exam_name;
                            Globals.exam_name = exam_name;
                        }

                        if (listexam_resp.resource_array[0].TryGetValue("exam_id", out exam_id))
                        {
                            string str_exam_id = Convert.ToString(exam_id);
                            examID.Text = examID.Text + Convert.ToString(str_exam_id);
                            Globals.exam_id = str_exam_id;
                        }

                        if (listexam_resp.resource_array[0].TryGetValue("status", out exam_status))
                        {
                            examStatus.Text = examStatus.Text + exam_status;
                            Globals.exam_status = exam_status;
                        }

                        if (listexam_resp.resource_array[0].TryGetValue("scheduled_date", out scheduled_date))
                        {
                            string str_scheduled_date = Convert.ToString(scheduled_date);
                            str_scheduled_date = str_scheduled_date.Replace("T", ", ");
                            scheduledDate.Text = scheduledDate.Text + str_scheduled_date;
                            Globals.exam_scheduled_date = str_scheduled_date;
                        }

                        if (listexam_resp.resource_array[0].TryGetValue("enrolled_students", out enrolled_students))
                        {
                            Globals.enrolled_students = enrolled_students;
                        }
                    }
                }
                else if (status_code == ((int)HttpStatusCode.Unauthorized))
                {
                    Console.WriteLine("Unauthorized");
                    //textBoxErrorMsg.Text = "Incorrect login details";
                }
                else if (status_code == ((int)HttpStatusCode.NotFound))
                {
                    Console.WriteLine("User not found");
                    //textBoxErrorMsg.Text = "User not found";
                }
                else if (status_code == ((int)HttpStatusCode.InternalServerError))
                {
                    Console.WriteLine("Internal server error occurred. Try again later.");
                    //textBoxErrorMsg.Text = "Internal server error occurred. Try again later.";
                }
            }
            catch (Exception exc)
            {
                Console.WriteLine("Application error occurred. Try again later: {0}", exc.Message);
                //textBoxErrorMsg.Text = "Application error occurred. Try again later.";
            }
        }

        private async void listExams()
        {
            try
            {
                var client = new RestClient("https://api.trustid-project.eu/backend/student/list_exam/");
                client.Timeout = -1;
                var request = new RestRequest(Method.GET);
                request.AddHeader("Content-Type", "application/json");
                request.AddHeader("Authorization", "Bearer " + Globals.jwt_access);

                IRestResponse restResponse = await client.ExecuteAsync(request);
                int status_code = (int)restResponse.StatusCode;

                if (status_code == ((int)HttpStatusCode.OK))
                {
                    Console.WriteLine("Success");
                    StudentListExamResponse listexam_resp = JsonConvert.DeserializeObject<StudentListExamResponse>(restResponse.Content);
                    Console.WriteLine("listexam resource_name: " + listexam_resp.resource_name);
                    Console.WriteLine("listexam resource_array: " + listexam_resp.resource_array);

                    if (listexam_resp.resource_array.Count > 0)
                    {
                        string exam_id = "";
                        string exam_status = "";
                        string scheduled_date = "";
                        string exam_name = "";
                        
                        if (listexam_resp.resource_array[0].TryGetValue("name", out exam_name))
                        {
                            examName.Text = examName.Text + exam_name;
                            Globals.exam_name = exam_name;
                        }

                        if (listexam_resp.resource_array[0].TryGetValue("exam_id", out exam_id))
                        {
                            examID.Text = examID.Text + exam_id;
                            Globals.exam_id = exam_id;
                        }

                        if (listexam_resp.resource_array[0].TryGetValue("status", out exam_status))
                        {
                            examStatus.Text = examStatus.Text + exam_status;
                            Globals.exam_status = exam_status;
                        }

                        if (listexam_resp.resource_array[0].TryGetValue("scheduled_date", out scheduled_date))
                        {
                            scheduled_date = scheduled_date.Replace("T", ", ");
                            scheduledDate.Text = scheduledDate.Text + scheduled_date;
                            Globals.exam_scheduled_date = scheduled_date;
                        }
                    }
                }
                else if (status_code == ((int)HttpStatusCode.Unauthorized))
                {
                    Console.WriteLine("Unauthorized");
                    //textBoxErrorMsg.Text = "Incorrect login details";
                }
                else if (status_code == ((int)HttpStatusCode.NotFound))
                {
                    Console.WriteLine("User not found");
                    //textBoxErrorMsg.Text = "User not found";
                }
                else if (status_code == ((int)HttpStatusCode.InternalServerError))
                {
                    Console.WriteLine("Internal server error occurred. Try again later.");
                    //textBoxErrorMsg.Text = "Internal server error occurred. Try again later.";
                }
            }
            catch (Exception exc)
            {
                Console.WriteLine("Application error occurred. Try again later: {0}", exc.Message);
                //textBoxErrorMsg.Text = "Application error occurred. Try again later.";
            }
        }

        private async void update_exam_condition()
        {
            try
            {
                var client = new RestClient("https://api.trustid-project.eu/backend/student/update_exam_condition/");
                client.Timeout = -1;
                var request = new RestRequest(Method.POST);
                request.AddHeader("Content-Type", "application/json");
                request.AddHeader("Authorization", "Bearer " + Globals.jwt_access);
                request.AddJsonBody(new
                {
                    condition = "Join",
                    exam_id = Globals.exam_id
                });
                IRestResponse restResponse = await client.ExecuteAsync(request);
                int status_code = (int)restResponse.StatusCode;

                if (status_code == ((int)HttpStatusCode.OK))
                {
                    Console.WriteLine("Success");
                    UpdateExamConditionResponse update_exam_resp = JsonConvert.DeserializeObject<UpdateExamConditionResponse>(restResponse.Content);
                    Console.WriteLine("Update exam resource_name: " + update_exam_resp.resource_name);
                    Console.WriteLine("Update exam message: " + update_exam_resp.message);
                }
                else if (status_code == ((int)HttpStatusCode.Unauthorized))
                {
                    Console.WriteLine("Unauthorized");
                    //textBoxErrorMsg.Text = "Incorrect login details";
                }
                else if (status_code == ((int)HttpStatusCode.NotFound))
                {
                    Console.WriteLine("User not found");
                    //textBoxErrorMsg.Text = "User not found";
                }
                else if (status_code == ((int)HttpStatusCode.InternalServerError))
                {
                    Console.WriteLine("Internal server error occurred. Try again later.");
                    //textBoxErrorMsg.Text = "Internal server error occurred. Try again later.";
                }
            }
            catch (Exception exc)
            {
                Console.WriteLine("Application error occurred. Try again later: {0}", exc.Message);
                //textBoxErrorMsg.Text = "Application error occurred. Try again later.";
            }
        }

        private void btnStartExam1_Click(object sender, RoutedEventArgs e)
        {
            // First update exam condition
            update_exam_condition();

            if (Globals.role == "student")
            {
                Enrollment newWindow = new Enrollment();
                newWindow.Show();
            }
            else
            {
                instructors_view newWindow = new instructors_view();
                newWindow.Show();
            }
        }

    }

}
