%% Import data from text file.
% Script for importing data from the following text file:
%
%    /Users/bsatheesh/Desktop/hw5/census-dataset/data.csv
%
% To extend the code to different selected data or a different text file,
% generate a function instead of a script.

% Auto-generated by MATLAB on 2015/11/04 00:09:04

%% Initialize variables.
filename = '/Users/bsatheesh/Desktop/hw5/census-dataset/data.csv';
delimiter = ',';
startRow = 2;

%% Format string for each line of text:
%   column1: double (%f)
%	column2: text (%s)
%   column3: double (%f)
%	column4: text (%s)
%   column5: double (%f)
%	column6: text (%s)
%   column7: text (%s)
%	column8: text (%s)
%   column9: text (%s)
%	column10: text (%s)
%   column11: double (%f)
%	column12: double (%f)
%   column13: double (%f)
%	column14: text (%s)
%   column15: double (%f)
% For more information, see the TEXTSCAN documentation.
formatSpec = '%f%s%f%s%f%s%s%s%s%s%f%f%f%s%f%[^\n\r]';

%% Open the text file.
fileID = fopen(filename,'r');

%% Read columns of data according to format string.
% This call is based on the structure of the file used to generate this
% code. If an error occurs for a different file, try regenerating the code
% from the Import Tool.
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);

%% Close the text file.
fclose(fileID);

%% Post processing for unimportable data.
% No unimportable data rules were applied during the import, so no post
% processing code is included. To generate code which works for
% unimportable data, select unimportable cells in a file and regenerate the
% script.

%% Create output variable
data = table(dataArray{1:end-1}, 'VariableNames', {'age','workclass','fnlwgt','education','educationnum','maritalstatus','occupation','relationship','race','sex','capitalgain','capitalloss','hoursperweek','nativecountry','label'});

%% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray ans;