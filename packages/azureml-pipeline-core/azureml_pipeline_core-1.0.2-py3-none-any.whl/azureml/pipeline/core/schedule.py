# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""schedule.py, module for defining schedule and schedule recurrence."""
from datetime import datetime
from enum import Enum
from azureml.pipeline.core.run import PipelineRun
from azureml.core import Experiment


class Schedule(object):
    """
    A Schedule submits a Pipeline on a specified recurrence schedule.

    :param workspace: Workspace object this Schedule will belong to.
    :type workspace: azureml.core.Workspace
    :param id: The id of the Schedule.
    :type id: str
    :param name: The name of the Schedule.
    :type name: str
    :param description: Description of the schedule.
    :type description: str
    :param pipeline_id: The id of the pipeline the schedule will submit.
    :type pipeline_id: str
    :param status: The status of the schedule.
    :type status: str
    :param recurrence: The recurrence for the schedule.
    :type recurrence: azureml.pipeline.core.graph.ScheduleRecurrence
    :param _schedule_provider: The schedule provider.
    :type _schedule_provider: _AevaScheduleProvider object
    """

    def __init__(self, workspace, id, name, description, pipeline_id, status, recurrence,
                 _schedule_provider=None):
        """
        Initialize Schedule.

        :param workspace: Workspace object this Schedule will belong to.
        :type workspace: azureml.core.Workspace
        :param id: The id of the Schedule.
        :type id: str
        :param name: The name of the Schedule.
        :type name: str
        :param description: Description of the schedule.
        :type description: str
        :param pipeline_id: The id of the pipeline the schedule will submit.
        :type pipeline_id: str
        :param status: The status of the schedule.
        :type status: str
        :param recurrence: The recurrence for the schedule.
        :type recurrence: azureml.pipeline.core.graph.ScheduleRecurrence
        :param _schedule_provider: The schedule provider.
        :type _schedule_provider: _AevaScheduleProvider object
        """
        self._id = id
        self._status = status
        self._name = name
        self._description = description
        self._recurrence = recurrence
        self._pipeline_id = pipeline_id
        self._workspace = workspace
        self._schedule_provider = _schedule_provider

    @property
    def id(self):
        """
        Get the ID for the schedule.

        :return: The ID.
        :rtype: str
        """
        return self._id

    @property
    def name(self):
        """
        Name of the schedule.

        :return: The name.
        :rtype: str
        """
        return self._name

    @property
    def description(self):
        """
        Get the description of the schedule.

        :return: The description string.
        :rtype: str
        """
        return self._description

    @property
    def pipeline_id(self):
        """
        Get the id of the pipeline the schedule submits.

        :return: The id.
        :rtype: str
        """
        return self._pipeline_id

    @property
    def status(self):
        """
        Status of the schedule.

        :return: The status.
        :rtype: str
        """
        return self._status

    @property
    def recurrence(self):
        """
        Get the schedule recurrence.

        :return: The schedule recurrence.
        :rtype: azureml.pipeline.core.graph.ScheduleRecurrence
        """
        return self._recurrence

    @staticmethod
    def create(workspace, name, pipeline_id, experiment_name, recurrence, description=None,
               pipeline_parameters=None, _workflow_provider=None, _service_endpoint=None):
        """
        Create a schedule.

        :param workspace: Workspace object this Schedule will belong to.
        :type workspace: azureml.core.Workspace
        :param name: The name of the Schedule.
        :type name: str
        :param pipeline_id: The id of the pipeline the schedule will submit.
        :type pipeline_id: str
        :param experiment_name: The name of the experiment the schedule will submit runs on.
        :type experiment_name: str
        :param recurrence: The recurrence for the schedule.
        :type recurrence: azureml.pipeline.core.graph.ScheduleRecurrence
        :param description: Description of the schedule.
        :type description: str
        :param pipeline_parameters: Dictionary of parameters to assign new values {param name, param value}
        :type pipeline_parameters: dict
        :param _workflow_provider: The workflow provider.
        :type _workflow_provider: _AevaWorkflowProvider object
        :param _service_endpoint: The service endpoint.
        :type _service_endpoint: str
        :return: The created schedule.
        :rtype: azureml.pipeline.core.graph.Schedule
        """
        recurrence.validate()

        from azureml.pipeline.core._graph_context import _GraphContext
        graph_context = _GraphContext('placeholder', workspace,
                                      workflow_provider=_workflow_provider,
                                      service_endpoint=_service_endpoint)
        return graph_context.workflow_provider.schedule_provider.create_schedule(name, pipeline_id,
                                                                                 experiment_name, recurrence,
                                                                                 description, pipeline_parameters)

    def update(self, name=None, description=None, recurrence=None, pipeline_parameters=None, status=None):
        """
        Update the schedule.

        :param name: The new name of the Schedule.
        :type name: str
        :param recurrence: The new recurrence for the schedule.
        :type recurrence: azureml.pipeline.core.graph.ScheduleRecurrence
        :param description: The new description of the schedule.
        :type description: str
        :param pipeline_parameters: Dictionary of parameters to assign new values {param name, param value}
        :type pipeline_parameters: dict
        :param status: The new status of the schedule: 'Active' or 'Disabled'.
        :type status: str
        """
        if recurrence is not None:
            recurrence.validate()

        if status is not None and status not in ['Active', 'Disabled']:
            raise ValueError('Status must be either Active or Disabled')

        new_schedule = self._schedule_provider.update_schedule(self.id, name=name, description=description,
                                                               status=status, recurrence=recurrence,
                                                               pipeline_parameters=pipeline_parameters)

        self._description = new_schedule.description
        self._name = new_schedule.name
        self._status = new_schedule.status
        self._recurrence = new_schedule.recurrence

    def activate(self):
        """Set the schedule to be 'Active' and available to run."""
        self._set_status('Active')

    def disable(self):
        """Set the schedule to be 'Disabled' and unavailable to run."""
        self._set_status('Disabled')

    def _set_status(self, new_status):
        """
        Set the schedule status.

        :param new_status: The new schedule status ('Active' or 'Disabled').
        :type new_status: str
        """
        self._schedule_provider.set_status(self._id, new_status)
        self._status = new_status

    def get_pipeline_runs(self):
        """
        Fetch the pipeline runs that were generated from the schedule.

        :return: a list of :class:`azureml.pipeline.core.run.PipelineRun`
        :rtype: list
        """
        run_tuples = self._schedule_provider.get_pipeline_runs_for_schedule(self._id)
        pipeline_runs = []
        for (run_id, experiment_name) in run_tuples:
            experiment = Experiment(self._workspace, experiment_name)
            pipeline_run = PipelineRun(experiment=experiment, run_id=run_id,
                                       _service_endpoint=self._schedule_provider._service_caller._service_endpoint)
            pipeline_runs.append(pipeline_run)

        return pipeline_runs

    def get_last_pipeline_run(self):
        """
        Fetch the last pipeline run submitted by the schedule. Returns None if no runs have been submitted.

        :return: The last pipeline run
        :rtype: azureml.pipeline.core.run.PipelineRun
        """
        run_id, experiment_name = self._schedule_provider.get_last_pipeline_run_for_schedule(self._id)
        if run_id is None:
            return None
        experiment = Experiment(self._workspace, experiment_name)
        return PipelineRun(experiment=experiment, run_id=run_id,
                           _service_endpoint=self._schedule_provider._service_caller._service_endpoint)

    @staticmethod
    def get_schedule(workspace, id, _workflow_provider=None, _service_endpoint=None):
        """
        Get the schedule.

        :param workspace: The workspace the schedule was created on.
        :type workspace: azureml.core.Workspace
        :param id: Id of the schedule.
        :type id: str
        :param _workflow_provider: The workflow provider.
        :type _workflow_provider: _AevaWorkflowProvider object
        :param _service_endpoint: The service endpoint.
        :type _service_endpoint: str

        :return: Schedule object
        :rtype: azureml.pipeline.core.graph.Schedule
        """
        from azureml.pipeline.core._graph_context import _GraphContext
        graph_context = _GraphContext('placeholder', workspace,
                                      workflow_provider=_workflow_provider,
                                      service_endpoint=_service_endpoint)
        return graph_context.workflow_provider.schedule_provider.get_schedule(schedule_id=id)

    @staticmethod
    def get_all(workspace, active_only=True, _workflow_provider=None, _service_endpoint=None):
        """
        Get all schedules in the current workspace.

        :param workspace: The workspace.
        :type workspace: azureml.core.Workspace
        :param active_only: If true, only return schedules which are currently active.
        :type active_only: Bool
        :param _workflow_provider: The workflow provider.
        :type _workflow_provider: _AevaWorkflowProvider object
        :param _service_endpoint: The service endpoint.
        :type _service_endpoint: str

        :return: a list of :class:`azureml.pipeline.core.graph.Schedule`
        :rtype: list
        """
        from azureml.pipeline.core._graph_context import _GraphContext
        graph_context = _GraphContext('placeholder', workspace,
                                      workflow_provider=_workflow_provider,
                                      service_endpoint=_service_endpoint)
        return graph_context.workflow_provider.schedule_provider.get_all_schedules(active_only=active_only)

    @staticmethod
    def get_schedules_for_pipeline_id(workspace, pipeline_id, _workflow_provider=None, _service_endpoint=None):
        """
        Get all schedules for the given pipeline id.

        :param workspace: The workspace.
        :type workspace: azureml.core.Workspace
        :param pipeline_id: The pipeline id.
        :type pipeline_id: str
        :param _workflow_provider: The workflow provider.
        :type _workflow_provider: _AevaWorkflowProvider object
        :param _service_endpoint: The service endpoint.
        :type _service_endpoint: str

        :return: a list of :class:`azureml.pipeline.core.graph.Schedule`
        :rtype: list
        """
        from azureml.pipeline.core._graph_context import _GraphContext
        graph_context = _GraphContext('placeholder', workspace,
                                      workflow_provider=_workflow_provider,
                                      service_endpoint=_service_endpoint)
        return graph_context.workflow_provider.schedule_provider.get_schedules_by_pipeline_id(pipeline_id=pipeline_id)


class ScheduleRecurrence(object):
    """
    A ScheduleRecurrence defines the frequency, interval and start time of a schedule.

    It also allows to specify the time zone and the hours or minutes or week days for the recurrence.

    :param frequency: The unit of time that describes how often the schedule fires.
                      Can be "Minute", "Hour", "Day", "Week", or  "Month"
    :type frequency: str
    :param interval: A value that specifies how often the schedule fires based on the frequency, which is the
                     number of time units to wait until the schedule fires again
    :type interval: int
    :param start_time: A datetime object which describes the start date and time. The tzinfo of the datetime object
                       should be none, use time_zone property to specify a time zone if needed. Can also be a
                       string in this format: YYYY-MM-DDThh:mm:ss. If None is provided the first workload is run
                       instantly and the future workloads are run based on the schedule. If the start time is
                       in the past, the first workload is run at the next calculated run time.
    :type start_time: datetime.datetime or str
    :param time_zone: Specify the time zone that you want to apply. If None is provided UTC is used.
    :type time_zone: azureml.pipeline.core.schedule.TimeZone
    :param hours: If you specify "Day" or "Week" for frequency, you can specify one or more integers from 0 to 23,
                  separated by commas, as the hours of the day when you want to run the workflow.
                  For example, if you specify "10", "12" and "14", you get 10 AM, 12 PM,
                  and 2 PM as the hour marks.
    :type hours: list of int
    :param minutes: If you specify "Day" or "Week" for frequency, you can specify one or more
                    integers from 0 to 59, separated by commas, as the minutes of the hour when you want to run
                    the workflow. For example, you can specify "30" as the minute mark and using the previous
                    example for hours of the day, you get 10:30 AM, 12:30 PM, and 2:30 PM.
    :type minutes: list of int
    :param week_days: If you specify "Week" for frequency, you can specify one or more days, separated by commas,
                      when you want to run the workflow: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                      "Saturday", and "Sunday"
    :type week_days: list of str
    """

    def __init__(self, frequency, interval, start_time=None, time_zone=None, hours=None, minutes=None, week_days=None):
        """
        Initialize a schedule recurrence.

        :param frequency: The unit of time that describes how often the schedule fires.
                          Can be "Minute", "Hour", "Day", "Week", or  "Month"
        :type frequency: str
        :param interval: A value that specifies how often the schedule fires based on the frequency, which is the
                         number of time units to wait until the schedule fires again
        :type interval: int
        :param start_time: A datetime object which describes the start date and time. The tzinfo of the datetime object
                           should be none, use time_zone property to specify a time zone if needed. Can also be a
                           string in this format: YYYY-MM-DDThh:mm:ss. If None is provided the first workload is run
                           instantly and the future workloads are run based on the schedule. If the start time is
                           in the past, the first workload is run at the next calculated run time.
        :type start_time: datetime.datetime or str
        :param time_zone: Specify the time zone that you want to apply. If None is provided UTC is used.
        :type time_zone: azureml.pipeline.core.schedule.TimeZone
        :param hours: If you specify "Day" or "Week" for frequency, you can specify one or more integers from 0 to 23,
                      separated by commas, as the hours of the day when you want to run the workflow.
                      For example, if you specify "10", "12" and "14", you get 10 AM, 12 PM,
                      and 2 PM as the hour marks.
        :type hours: list of int
        :param minutes: If you specify "Day" or "Week" for frequency, you can specify one or more
                        integers from 0 to 59, separated by commas, as the minutes of the hour when you want to run
                        the workflow. For example, you can specify "30" as the minute mark and using the previous
                        example for hours of the day, you get 10:30 AM, 12:30 PM, and 2:30 PM.
        :type minutes: list of int
        :param week_days: If you specify "Week" for frequency, you can specify one or more days, separated by commas,
                          when you want to run the workflow: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                          "Saturday", and "Sunday"
        :type week_days: list of str
        """
        self.frequency = frequency
        self.interval = interval
        self.start_time = None
        if start_time is not None:
            if isinstance(start_time, datetime):
                if start_time.tzinfo is not None:
                    raise ValueError('Can not specify tzinfo for start_time, use time_zone instead.')
                self.start_time = start_time.isoformat()
            else:
                self.start_time = start_time
        self.time_zone = time_zone
        if self.start_time is not None and self.time_zone is None:
            self.time_zone = TimeZone.GMTStandardTime
        self.hours = hours
        self.minutes = minutes
        self.week_days = week_days

    def validate(self):
        """
        Validate the schedule recurrence.
        """
        if self.frequency not in ["Minute", "Hour", "Day", "Week", "Month"]:
            raise ValueError("Invalid value for frequency, only one of Minute, Hour, Day, "
                             "Week, or Month accepted")
        if self.interval < 1:
            raise ValueError("Interval must be an integer greater than 0.")
        if self.frequency not in ["Day", "Week"] and self.hours is not None:
            raise ValueError("Can only specify hours if frequency is Week or Day.")
        if self.frequency not in ["Day", "Week"] and self.minutes is not None:
            raise ValueError("Can only specify minutes if frequency is Week or Day.")
        if self.frequency != "Week" and self.week_days is not None:
            raise ValueError("Can only specify week days if frequency is Week.")
        if self.hours is not None:
            for hour in self.hours:
                if hour < 0 or hour > 23:
                    raise ValueError("Hours must be a list of integers between 0 and 23.")
        if self.minutes is not None:
            for minute in self.minutes:
                if minute < 0 or minute > 59:
                    raise ValueError("Minutes must be a list of integers between 0 and 59.")
        if self.week_days is not None:
            for week_day in self.week_days:
                if week_day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                    raise ValueError("Week days must be a list of str, accpeted values: Monday, Tuesday, Wednesday, "
                                     "Thursday, Friday, Saturday, Sunday.")
        if self.time_zone is not None and not isinstance(self.time_zone, TimeZone):
            raise ValueError("Time zone is not a valid TimeZone enum.")
        if self.start_time is not None and self.time_zone is None:
            raise ValueError('Must specify time_zone if start_time is provided.')


class TimeZone(Enum):
    """Enumerates the valid time zones for a schedule."""
    DatelineStandardTime = "Dateline Standard Time"
    UTC11 = "UTC-11"
    AleutianStandardTime = "Aleutian Standard Time"
    HawaiianStandardTime = "Hawaiian Standard Time"
    MarquesasStandardTime = "Marquesas Standard Time"
    AlaskanStandardTime = "Alaskan Standard Time"
    UTC09 = "UTC-09"
    PacificStandardTimeMexico = "Pacific Standard Time (Mexico)"
    UTC08 = "UTC-08"
    PacificStandardTime = "Pacific Standard Time"
    USMountainStandardTime = "US Mountain Standard Time"
    MountainStandardTimeMexico = "Mountain Standard Time (Mexico)"
    MountainStandardTime = "Mountain Standard Time"
    CentralAmericaStandardTime = "Central America Standard Time"
    CentralStandardTime = "Central Standard Time"
    EasterIslandStandardTime = "Easter Island Standard Time"
    CentralStandardTimeMexico = "Central Standard Time (Mexico)"
    CanadaCentralStandardTime = "Canada Central Standard Time"
    SAPacificStandardTime = "SA Pacific Standard Time"
    EasternStandardTimeMexico = "Eastern Standard Time (Mexico)"
    EasternStandardTime = "Eastern Standard Time"
    HaitiStandardTime = "Haiti Standard Time"
    CubaStandardTime = "Cuba Standard Time"
    USEasternStandardTime = "US Eastern Standard Time"
    ParaguayStandardTime = "Paraguay Standard Time"
    AtlanticStandardTime = "Atlantic Standard Time"
    VenezuelaStandardTime = "Venezuela Standard Time"
    CentralBrazilianStandardTime = "Central Brazilian Standard Time"
    SAWesternStandardTime = "SA Western Standard Time"
    PacificSAStandardTime = "Pacific SA Standard Time"
    TurksAndCaicosStandardTime = "Turks And Caicos Standard Time"
    NewfoundlandStandardTime = "Newfoundland Standard Time"
    TocantinsStandardTime = "Tocantins Standard Time"
    ESouthAmericaStandardTime = "E. South America Standard Time"
    SAEasternStandardTime = "SA Eastern Standard Time"
    ArgentinaStandardTime = "Argentina Standard Time"
    GreenlandStandardTime = "Greenland Standard Time"
    MontevideoStandardTime = "Montevideo Standard Time"
    SaintPierreStandardTime = "Saint Pierre Standard Time"
    BahiaStandardTime = "Bahia Standard Time"
    UTC02 = "UTC-02"
    MidAtlanticStandardTime = "Mid-Atlantic Standard Time"
    AzoresStandardTime = "Azores Standard Time"
    CapeVerdeStandardTime = "Cape Verde Standard Time"
    UTC = "UTC"
    MoroccoStandardTime = "Morocco Standard Time"
    GMTStandardTime = "GMT Standard Time"
    GreenwichStandardTime = "Greenwich Standard Time"
    WEuropeStandardTime = "W. Europe Standard Time"
    CentralEuropeStandardTime = "Central Europe Standard Time"
    RomanceStandardTime = "Romance Standard Time"
    CentralEuropeanStandardTime = "Central European Standard Time"
    WCentralAfricaStandardTime = "W. Central Africa Standard Time"
    NamibiaStandardTime = "Namibia Standard Time"
    JordanStandardTime = "Jordan Standard Time"
    GTBStandardTime = "GTB Standard Time"
    MiddleEastStandardTime = "Middle East Standard Time"
    EgyptStandardTime = "Egypt Standard Time"
    EEuropeStandardTime = "E. Europe Standard Time"
    SyriaStandardTime = "Syria Standard Time"
    WestBankStandardTime = "West Bank Standard Time"
    SouthAfricaStandardTime = "South Africa Standard Time"
    FLEStandardTime = "FLE Standard Time"
    TurkeyStandardTime = "Turkey Standard Time"
    IsraelStandardTime = "Israel Standard Time"
    KaliningradStandardTime = "Kaliningrad Standard Time"
    LibyaStandardTime = "Libya Standard Time"
    ArabicStandardTime = "Arabic Standard Time"
    ArabStandardTime = "Arab Standard Time"
    BelarusStandardTime = "Belarus Standard Time"
    RussianStandardTime = "Russian Standard Time"
    EAfricaStandardTime = "E. Africa Standard Time"
    IranStandardTime = "Iran Standard Time"
    ArabianStandardTime = "Arabian Standard Time"
    AstrakhanStandardTime = "Astrakhan Standard Time"
    AzerbaijanStandardTime = "Azerbaijan Standard Time"
    RussiaTimeZone3 = "Russia Time Zone 3"
    MauritiusStandardTime = "Mauritius Standard Time"
    GeorgianStandardTime = "Georgian Standard Time"
    CaucasusStandardTime = "Caucasus Standard Time"
    AfghanistanStandardTime = "Afghanistan Standard Time"
    WestAsiaStandardTime = "West Asia Standard Time"
    EkaterinburgStandardTime = "Ekaterinburg Standard Time"
    PakistanStandardTime = "Pakistan Standard Time"
    IndiaStandardTime = "India Standard Time"
    SriLankaStandardTime = "Sri Lanka Standard Time"
    NepalStandardTime = "Nepal Standard Time"
    CentralAsiaStandardTime = "Central Asia Standard Time"
    BangladeshStandardTime = "Bangladesh Standard Time"
    NCentralAsiaStandardTime = "N. Central Asia Standard Time"
    MyanmarStandardTime = "Myanmar Standard Time"
    SEAsiaStandardTime = "SE Asia Standard Time"
    AltaiStandardTime = "Altai Standard Time"
    WMongoliaStandardTime = "W. Mongolia Standard Time"
    NorthAsiaStandardTime = "North Asia Standard Time"
    TomskStandardTime = "Tomsk Standard Time"
    ChinaStandardTime = "China Standard Time"
    NorthAsiaEastStandardTime = "North Asia East Standard Time"
    SingaporeStandardTime = "Singapore Standard Time"
    WAustraliaStandardTime = "W. Australia Standard Time"
    TaipeiStandardTime = "Taipei Standard Time"
    UlaanbaatarStandardTime = "Ulaanbaatar Standard Time"
    NorthKoreaStandardTime = "North Korea Standard Time"
    AusCentralWStandardTime = "Aus Central W. Standard Time"
    TransbaikalStandardTime = "Transbaikal Standard Time"
    TokyoStandardTime = "Tokyo Standard Time"
    KoreaStandardTime = "Korea Standard Time"
    YakutskStandardTime = "Yakutsk Standard Time"
    CenAustraliaStandardTime = "Cen. Australia Standard Time"
    AUSCentralStandardTime = "AUS Central Standard Time"
    EAustraliaStandardTime = "E. Australia Standard Time"
    AUSEasternStandardTime = "AUS Eastern Standard Time"
    WestPacificStandardTime = "West Pacific Standard Time"
    TasmaniaStandardTime = "Tasmania Standard Time"
    VladivostokStandardTime = "Vladivostok Standard Time"
    LordHoweStandardTime = "Lord Howe Standard Time"
    BougainvilleStandardTime = "Bougainville Standard Time"
    RussiaTimeZone10 = "Russia Time Zone 10"
    MagadanStandardTime = "Magadan Standard Time"
    NorfolkStandardTime = "Norfolk Standard Time"
    SakhalinStandardTime = "Sakhalin Standard Time"
    CentralPacificStandardTime = "Central Pacific Standard Time"
    RussiaTimeZone11 = "Russia Time Zone 11"
    NewZealandStandardTime = "New Zealand Standard Time"
    UTC12 = "UTC+12"
    FijiStandardTime = "Fiji Standard Time"
    KamchatkaStandardTime = "Kamchatka Standard Time"
    ChathamIslandsStandardTime = "Chatham Islands Standard Time"
    TongaStandardTime = "Tonga Standard Time"
    SamoaStandardTime = "Samoa Standard Time"
    LineIslandsStandardTime = "Line Islands Standard Time"
