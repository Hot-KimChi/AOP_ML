
    def fn_diff_check(self):
        mae = mean_absolute_error(self.test_target, self.prediction)
        print('|(타깃 - 예측값)|:', mae)

        Diff = np.round_(self.prediction - self.test_target, 2)
        Diff_per = np.round_((self.test_target - self.prediction) / self.test_target * 100, 1)

        bad = 0
        good = 0
        print()

        df_bad = pd.DataFrame()
        failed_condition = pd.DataFrame()

        df = pd.DataFrame()
        pass_condition = pd.DataFrame()

        # df_test_input = pd.DataFrame(test_input, columns=['txFrequencyHz',
        #                                                                          'focusRangeCm',
        #                                                                          'numTxElements',
        #                                                                          'txpgWaveformStyle',
        #                                                                          'numTxCycles',
        #                                                                          'elevAperIndex',
        #                                                                          'IsTxAperModulationEn',
        #                                                                          'probePitchCm',
        #                                                                          'probeRadiusCm',
        #                                                                          'probeElevAperCm0',
        #                                                                          'probeElevFocusRangCm'])
        #
        # func_show_table('test_input', df=df_test_input)


        for i in range(len(Diff)):
            if abs(Diff[i]) > 1:
                bad = bad + 1

                df_bad = df_bad.append \
                    (pd.DataFrame([[i, self.test_target[i], self.prediction[i], Diff[i], Diff_per[i]]],
                                                    columns=['index', '측정값(Cm)', '예측값(Cm)', 'Diff(Cm)', 'Diff(%)']),
                                       ignore_index=True)
                # df_bad_sort_values = df_bad.sort_values(by=df_bad.columns[3], ascending=True)
                # df_bad_sort_values = df_bad_sort_values.reset_index(drop=True)

                failed_condition = failed_condition.append(pd.DataFrame([self.test_input[i]],
                                                                        columns=self.feature_list),
                                                           ignore_index=True)

            else:
                good = good + 1

                df = df.append(pd.DataFrame([[i, self.test_target[i], self.prediction[i], Diff[i], Diff_per[i]]],
                                            columns=['index', 'target', 'expect', 'Diff(Cm)', 'Diff(%)']),
                               ignore_index=True)
                # df_sort_values = df.sort_values(by=df.columns[3], ascending=True)
                # df_sort_values = df_sort_values.reset_index(drop=True)

                pass_condition = pass_condition.append(pd.DataFrame([self.test_input[i]],
                                                                    columns=self.feature_list),
                                                       ignore_index=True)

        print()
        print('bad:', bad)
        print('good:', good)

        merge_bad_inner = pd.concat([df_bad, failed_condition], axis=1)
        merge_good_inner = pd.concat([df, pass_condition], axis=1)

        ## failed condition show-up
        ShowTable.fn_show_table("failed_condition", df=merge_bad_inner if len(merge_bad_inner.index) > 0 else None)

        ShowTable.fn_show_table("pass_condition", df=merge_good_inner if len(merge_good_inner.index) > 0 else None)

