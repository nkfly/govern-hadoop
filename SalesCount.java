package org.myorg;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;

public class SalesCount {

    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, IntWritable> {
      private final static IntWritable one = new IntWritable(1);

      public void map(LongWritable key, Text value, OutputCollector<Text, IntWritable> output, Reporter reporter) throws IOException {
        String line = value.toString();
        String [] entries = line.split(";");
        boolean hasOrder = entries[1].indexOf("act=order") == -1 ? false : true;
        if (hasOrder) {
          //String [] plist_entries = entries[3].split("=");

		String [] plist = entries[3].substring(5).split(",");

          for (int i = 0;i < plist.length/3;i++){
            Text word = new Text();
            word.set(plist[3*i]);
            output.collect(word, new IntWritable(-Integer.valueOf(plist[3*i+1])*Integer.valueOf(plist[3*i+2])  ));
          }
        }
      }
    }

    public static class Reduce extends MapReduceBase implements Reducer<Text, IntWritable, IntWritable, Text> {
      public void reduce(Text key, Iterator<IntWritable> values, OutputCollector<IntWritable, Text> output, Reporter reporter) throws IOException {
        int sum = 0;
        while (values.hasNext()) {
          sum += values.next().get();
        }
        output.collect(new IntWritable(sum),key);
      }
    }

    public static void main(String[] args) throws Exception {
      JobConf conf = new JobConf(SalesCount.class);
      conf.setJobName("salescount");

      conf.setOutputKeyClass(Text.class);
      conf.setOutputValueClass(IntWritable.class);

      conf.setMapperClass(Map.class);
      conf.setCombinerClass(Reduce.class);
      conf.setReducerClass(Reduce.class);

      conf.setInputFormat(TextInputFormat.class);
      conf.setOutputFormat(TextOutputFormat.class);

      FileInputFormat.setInputPaths(conf, new Path(args[0]));
      FileOutputFormat.setOutputPath(conf, new Path(args[1]));

      JobClient.runJob(conf);
    }
}

