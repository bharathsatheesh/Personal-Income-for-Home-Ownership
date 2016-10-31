%% Impurity using info-gain
function imba = Impurity(left_label_hist,right_label_hist)
            %Entropy for the left child
            len_l = length(left_label_hist);
            p_l = sum(left_label_hist)/len_l;
            if (p_l == 0) || (p_l ==1)
                e_l = 0;
            else
            q_l = 1-p_l;
            e_l = -1*(p_l*log2(p_l) + q_l*log2(q_l));
            end
            %Entropy for the right child
            len_r = length(right_label_hist);
            p_r = sum(right_label_hist)/len_r;
            if (p_r == 0) || (p_r ==1)
                e_r = 0;
            else
            q_r = 1-p_r;
            e_r = -1*(p_r*log2(p_r) + q_r*log2(q_r));
            end
            %Entropy for the parent
            len = len_l + len_r;
            p_p = (sum(left_label_hist) + sum(right_label_hist))/len;
            q_p = 1 - p_p;
            e_p = -10 * (p_p*log2(p_p) + q_p*log2(q_p));
            weighed_ent = (len_l*e_l + len_r*e_r)/len;
            imba = e_p - weighed_ent;
            %imba = abs(imba);
            
        end