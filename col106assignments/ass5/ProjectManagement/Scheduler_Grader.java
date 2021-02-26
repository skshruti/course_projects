package ProjectManagement;

import java.io.*;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class Scheduler_Grader {
    private  static Scheduler_Driver scheduler_driver;

    private static ArrayList<Long> user_time, job_time,project_time,rtc_time,job_report_time,user_report_time, flush_time;


    public static void main(String[] args) throws FileNotFoundException {

        user_time = new ArrayList<>();
        job_time = new ArrayList<>();
        project_time = new ArrayList<>();
        rtc_time = new ArrayList<>();
        job_report_time = new ArrayList<>();
        user_report_time = new ArrayList<>();
        flush_time = new ArrayList<>();

        // Creating a File object that represents the disk file.
        PrintStream o = new PrintStream(new File("tmp_output"));
        // Store current System.out before assigning a new value
        PrintStream console = System.out;
        // Assign o to output stream
        Boolean debug = true;
        debug = false;
        if(!debug)
        System.setOut(o);

        scheduler_driver = new Scheduler_Driver();
        File file;
        if (args.length == 0) {
            URL url = Scheduler_Driver.class.getResource("INP");
            file = new File(url.getPath());
        } else {
            file = new File(args[0]);
        }

        try {
            execute(file);
        } catch (IOException e) {
            e.printStackTrace();
        }

        if(!debug) {
            System.setOut(console);
            System.out.println("Queries executed successfully");
            System.out.println("Job report average time: "+calculateAverage(job_report_time));
            System.out.println("User report average time: "+calculateAverage(user_report_time));
            System.out.println("Flush report average time: "+calculateAverage(flush_time));
            System.out.println();
        }
    }
    static void execute(File commandFile) throws IOException {


        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(commandFile));

            String st;
            while ((st = br.readLine()) != null) {
                String[] cmd = st.split(" ");
                if (cmd.length == 0) {
                    System.err.println("Error parsing: " + st);
                    return;
                }
                String project_name, user_name;
                Integer start_time, end_time;

                long qstart_time, qend_time;

                switch (cmd[0]) {
                    case "PROJECT":
                        scheduler_driver.timed_handle_project(cmd);
                        break;
                    case "JOB":
                        scheduler_driver.timed_handle_job(cmd);
                        break;
                    case "USER":
                        scheduler_driver.timed_handle_user(cmd[1]);
                        break;
                    case "QUERY":
                        scheduler_driver.handle_query(cmd[1]);
                        break;
                    case "":
                        scheduler_driver.handle_empty_line();
                        break;
                    case "ADD":
                        scheduler_driver.handle_add(cmd);
                        break;
                    //--------- New Queries
                    case "NEW_USER":
                    case "NEW_PROJECT":
                    case "NEW_PROJECTUSER":
                    case "NEW_PRIORITY":
                        qstart_time = System.nanoTime();
                        ArrayList<JobReport_>  out_user = scheduler_driver.timed_report(cmd);
                        qend_time = System.nanoTime();
                        System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));
                        job_report_time.add(qend_time-qstart_time);
                        break;

                    case "NEW_TOP":
                        qstart_time = System.nanoTime();
                        ArrayList<UserReport_>  out_topuser  =scheduler_driver.timed_top_consumer(Integer.parseInt(cmd[1]));
                        qend_time = System.nanoTime();
                        System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));
                        user_report_time.add(qend_time-qstart_time);

                        break;
                    case "NEW_FLUSH":
                        qstart_time = System.nanoTime();
                        scheduler_driver.timed_flush(Integer.parseInt(cmd[1]));
                        qend_time = System.nanoTime();
                        flush_time.add(qend_time-qstart_time);
                        break;
                    default:
                        System.err.println("Unknown command: " + cmd[0]);
                }
            }


            scheduler_driver.timed_run_to_completion();
            scheduler_driver.print_stats();

        } catch (FileNotFoundException e) {
            System.err.println("Input file Not found. " + commandFile.getAbsolutePath());
        } catch (NullPointerException ne) {
            ne.printStackTrace();

        }
    }

    private static double calculateAverage(List<Long> longs) {
        Long sum = 0l;
        if(!longs.isEmpty()) {
            for (Long mark : longs) {
                sum += mark;
            }
            return sum.doubleValue() / longs.size();
        }
        return sum;
    }
}