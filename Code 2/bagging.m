%% Bagging implementation

function [r_data, r_labels] = bagging(data,labels)
    [len, wid] = size(data);
    sample_count = 0.3*len;
    sample_count = double(sample_count);
    collab = [data,labels];
    index = randsample((1:len),sample_count);
    collab = collab(index,:);
    r_data = collab(:,1:wid);
    r_labels = collab(:,wid+1);
   
    