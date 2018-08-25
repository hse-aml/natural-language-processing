from collections import OrderedDict

def _update_chunk(candidate, prev, current_tag, current_chunk, current_pos, prediction=False):
    if candidate == 'B-' + current_tag:
        if len(current_chunk) > 0 and len(current_chunk[-1]) == 1:
                current_chunk[-1].append(current_pos - 1)
        current_chunk.append([current_pos])
    elif candidate == 'I-' + current_tag:
        if prediction and (current_pos == 0 or current_pos > 0 and prev.split('-', 1)[-1] != current_tag):
            current_chunk.append([current_pos])
        if not prediction and (current_pos == 0 or current_pos > 0 and prev == 'O'):
            current_chunk.append([current_pos])
    elif current_pos > 0 and prev.split('-', 1)[-1] == current_tag:
        if len(current_chunk) > 0:
            current_chunk[-1].append(current_pos - 1)

def _update_last_chunk(current_chunk, current_pos):
    if len(current_chunk) > 0 and len(current_chunk[-1]) == 1:
        current_chunk[-1].append(current_pos - 1)

def _tag_precision_recall_f1(tp, fp, fn):
    precision, recall, f1 = 0, 0, 0
    if tp + fp > 0:
        precision = tp / (tp + fp) * 100
    if tp + fn > 0:
        recall = tp / (tp + fn) * 100
    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1

def _aggregate_metrics(results, total_correct):
    total_true_entities = 0
    total_predicted_entities = 0
    total_precision = 0
    total_recall = 0
    total_f1 = 0
    for tag, tag_metrics in results.items():
        n_pred = tag_metrics['n_predicted_entities']
        n_true = tag_metrics['n_true_entities']
        total_true_entities += n_true
        total_predicted_entities += n_pred
        total_precision += tag_metrics['precision'] * n_pred
        total_recall += tag_metrics['recall'] * n_true
    
    accuracy = 0
    if total_true_entities > 0:
        accuracy = total_correct / total_true_entities * 100
    else:
        print('CAUTION! Accuracy equals zero because there are no '\
              'correct entities. Check the correctness of your data.')
    if total_predicted_entities > 0:
        total_precision = total_precision / total_predicted_entities
    total_recall = total_recall / total_true_entities
    if total_precision + total_recall > 0:
        total_f1 = 2 * total_precision * total_recall / (total_precision + total_recall)
    return total_true_entities, total_predicted_entities, \
           total_precision, total_recall, total_f1, accuracy

def _print_info(n_tokens, total_true_entities, total_predicted_entities, total_correct):
    print('processed {len} tokens ' \
          'with {tot_true} phrases; ' \
          'found: {tot_pred} phrases; ' \
          'correct: {tot_cor}.\n'.format(len=n_tokens,
                                         tot_true=total_true_entities,
                                         tot_pred=total_predicted_entities,
                                         tot_cor=total_correct))

def _print_metrics(accuracy, total_precision, total_recall, total_f1):
    print('precision:  {tot_prec:.2f}%; ' \
          'recall:  {tot_recall:.2f}%; ' \
          'F1:  {tot_f1:.2f}\n'.format(acc=accuracy,
                                           tot_prec=total_precision,
                                           tot_recall=total_recall,
                                           tot_f1=total_f1))

def _print_tag_metrics(tag, tag_results):
    print(('\t%12s' % tag) + ': precision:  {tot_prec:6.2f}%; ' \
                               'recall:  {tot_recall:6.2f}%; ' \
                               'F1:  {tot_f1:6.2f}; ' \
                               'predicted:  {tot_predicted:4d}\n'.format(tot_prec=tag_results['precision'],
                                                                         tot_recall=tag_results['recall'],
                                                                         tot_f1=tag_results['f1'],
                                                                         tot_predicted=tag_results['n_predicted_entities']))

def precision_recall_f1(y_true, y_pred, print_results=True, short_report=False):
    # Find all tags
    tags = sorted(set(tag[2:] for tag in y_true + y_pred if tag != 'O'))

    results = OrderedDict((tag, OrderedDict()) for tag in tags)
    n_tokens = len(y_true)
    total_correct = 0

    # For eval_conll_try we find all chunks in the ground truth and prediction
    # For each chunk we store starting and ending indices
    for tag in tags:
        true_chunk = list()
        predicted_chunk = list()
        for position in range(n_tokens):
            _update_chunk(y_true[position], y_true[position - 1], tag, true_chunk, position)
            _update_chunk(y_pred[position], y_pred[position - 1], tag, predicted_chunk, position, True)

        _update_last_chunk(true_chunk, position)
        _update_last_chunk(predicted_chunk, position)

        # Then we find all correctly classified intervals
        # True positive results
        tp = sum(chunk in predicted_chunk for chunk in true_chunk)
        total_correct += tp

        # And then just calculate errors of the first and second kind
        # False negative
        fn = len(true_chunk) - tp
        # False positive
        fp = len(predicted_chunk) - tp
        precision, recall, f1 = _tag_precision_recall_f1(tp, fp, fn)

        results[tag]['precision'] = precision
        results[tag]['recall'] = recall
        results[tag]['f1'] = f1
        results[tag]['n_predicted_entities'] = len(predicted_chunk)
        results[tag]['n_true_entities'] = len(true_chunk)

    total_true_entities, total_predicted_entities, \
           total_precision, total_recall, total_f1, accuracy = _aggregate_metrics(results, total_correct)

    if print_results:
        _print_info(n_tokens, total_true_entities, total_predicted_entities, total_correct)
        _print_metrics(accuracy, total_precision, total_recall, total_f1)

        if not short_report:
            for tag, tag_results in results.items():
                _print_tag_metrics(tag, tag_results)
    return results
