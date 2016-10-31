function [indices, threshold,tempo] = Segmentor(data,labels)
            [~, wid] = size(data);
            tempo = zeros(wid,1);
            return_threshold = zeros(wid,1);
            for index = 1:wid
                select_col = data(:,index);
                unique_col = unique(select_col);
                temp = ones(length(unique_col),1);
                for i = 1:length(unique_col)
                    left_label_hist = labels(select_col > unique_col(i));
                    right_label_hist = labels(select_col <= unique_col(i));
                    temp(i) = Impurity(left_label_hist,right_label_hist);
                end
                [tempo(index), index_val] = max(temp);
                return_threshold(index) = unique_col(index_val);
            end
            [~, indices] = max(tempo);
            threshold = return_threshold(indices);
        end