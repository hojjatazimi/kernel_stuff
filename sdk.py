""" Runs the task from the menu """
import logging
from datetime import datetime
from importlib.metadata import version as get_version

import numpy as np
import pandas as pd
from kernel.sdk.task import TaskClient
from kernel.sdk.task_registry import TaskRegistry
from kernel.tasks.tap.params import TapParams
from kernel.tasks.tap.prompts import TapPrompts
from psychopy import core, event

logger = logging.getLogger(__name__)
event.globalKeys.add(key="c", modifiers=["ctrl"], func=core.quit)
event.globalKeys.add(key="escape", func=core.quit)


def run_task(params: TapParams, prompts: TapPrompts, practice: bool):
    tc = TaskClient(
        multicast_ip=params.ip,
        multicast_port=params.port,
        debug=params.debug_mode,
        enforce_registry_entry=not practice,
        experiment_name="finger_tapping",
        experiment_version=get_version("kernel.tasks.tap"),
    )

    params.send_params(tc)

    # start experiment
    block_stim_info = prompts.practice_block_stim_info if practice else prompts.block_stim_info
    exp_type = "practice" if practice else TaskRegistry.FT02

    quit_request = False

    with tc.experiment(type=exp_type):
        logger.info(f"starting experiment with type {exp_type}")

        # baseline rest period
        if not practice:
            logger.info("initial rest period")
            prompts.win_flip()
            prompts.draw_fixation()
            prompts.win_flip()
            tc.rest(params.baseline_dur)

        # loop through blocks
        for b_type, t_types in block_stim_info:

            prompts.draw_hand(b_type)
            prompts.win_flip()

            # start block
            with tc.block(type=b_type):

                # loop through trials
                for idx_trial, t_type in enumerate(t_types):

                    # ITI
                    with tc.event("ITI"):
                        ITI_dur = np.random.normal(loc=params.ITI_dur_mean, scale=params.ITI_dur_std, size=1)[0]
                        keypresses = event.waitKeys(maxWait=abs(ITI_dur), keyList=params.quit_keys, clearEvents=True)

                    if keypresses:
                        quit_request = True
                        break

                    # start trial
                    with tc.trial(type=t_type):
                        # draw hand + finger cue
                        prompts.draw_hand(b_type)
                        prompts.draw_finger_cue(b_type, t_type)
                        prompts.win_flip()
                        keypresses = event.waitKeys(maxWait=params.tap_dur, keyList=params.quit_keys, clearEvents=True)
                        logger.info(f"tap with type {t_type}")
                        prompts.draw_hand(b_type) if idx_trial != len(t_types) - 1 else prompts.draw_fixation()
                        prompts.win_flip()

                    if keypresses:
                        quit_request = True
                        break
            if quit_request:
                break

            # ease transition b/w blocks
            if practice:
                core.wait(1)
                prompts.win_flip()
            else:
                # rest
                logger.info("rest")
                prompts.draw_fixation()
                prompts.win_flip()
                tc.rest(params.rest_dur)

        if not practice and not quit_request:
            tc.rest(params.end_baseline_dur)

    if practice:
        prompts.draw_end_practice(wait=True)
    else:
        prompts.draw_finished(ease_in=0.5)

    if params.debug_mode:
        df_out = pd.DataFrame(tc.debug_events)
        df_out.timestamp *= 1e-9
        df_out.to_csv(f'task_df_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv', index=False)

    logger.info("ending experiment")
