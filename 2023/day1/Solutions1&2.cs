using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace ConsoleApp1
{
    class Program
    {

        static void Main(string[] args)
        {
            int total = 0;

            total = ParseTextFile();
            Console.WriteLine(total);
        }


        private static int ParseTextFile()
        {
            const Int32 BufferSize = 128;
            int total = 0;

            //for Solution 1 -> replace TextFile2 with TextFile1
            using (var fileStream = File.OpenRead("C:/Users/hegarmai/source/repos/ConsoleApp1/ConsoleApp1/TextFile2.txt"))
            using (var streamReader = new StreamReader(fileStream, Encoding.UTF8, true, BufferSize))
            {
                String line;
                while ((line = streamReader.ReadLine()) != null)
                {
                    //Solution 1 -> replace with TextFile1
                    //Get2DigitValue(line)
                    //Solution 2
                    int s = Get2DigitsFromWordNums(line);
                    Console.WriteLine(s);
                    total += s;
                }
            }
            return total;
        }
        private static int Get2DigitsFromWordNums(string s)
        {
            string[] stringNums = new string[] { "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" };
            List<string> numStringArray = new List<string>();
            string stringNum = "";
            int intNum = 0;

            int digit;
            for (int i = 0; i < s.Length; i++)
            {

                int checkNum;
                string c = s[i].ToString();

                if (int.TryParse(c, out checkNum))//check if char is a number first
                {
                    numStringArray.Add(c);
                }
                else //if not check if there is a number in word form
                {
                    for (int j = 0; j < stringNums.Length; j++)
                    {
                        digit = ReturnNumIfWordIsNumber(s, i, stringNums[j], j + 1);
                        if (digit > 0)
                            numStringArray.Add(digit.ToString());
                    }
                }
            }

            if (numStringArray.Count > 0)
            {
                stringNum = numStringArray.First() + numStringArray.Last();
                intNum = int.Parse(stringNum);
            }

            return intNum;
        }

        private static int ReturnNumIfWordIsNumber(string input, int startIndex, string digitString, int numberMatch)
        {
            int num = 0;

            if (digitString.Length <= (input.Length - (startIndex)))// do not attempt if not enough chars left in string to compare to digitString
            {
                string compString = input.Substring(startIndex, digitString.Length);

                if (compString.Equals(digitString))
                {
                    return numberMatch;
                }
            }

            return num;
        }

        private static int Get2DigitValue(string s)
        {
            List<string> numStringArray = new List<string>();
            string stringNum = "";
            int intNum = 0;
            for (int i = 0; i < s.Length; i++)
            {
                int checkNum;
                string c = s[i].ToString();

                if (int.TryParse(c, out checkNum))
                {
                    numStringArray.Add(c);
                }
            }
            if (numStringArray.Count > 0)
            {
                stringNum = numStringArray.First() + numStringArray.Last();
                intNum = int.Parse(stringNum);
            }

            return intNum;
        }
    }
}
