# Reference

## Table of Contents

- [History](#history)
- [TextToSoundEffects](#texttosoundeffects)
- [AudioIsolation](#audioisolation)
- [Samples](#samples)
- [TextToSpeech](#texttospeech)
- [TextToDialogue](#texttodialogue)
- [SpeechToSpeech](#speechtospeech)
- [TextToVoice](#texttovoice)
- [user](#user)
- [Voices](#voices)
- [Studio](#studio)
- [Dubbing](#dubbing)
- [Models](#models)
- [AudioNative](#audionative)
- [usage](#usage)
- [PronunciationDictionaries](#pronunciationdictionaries)
- [ServiceAccounts](#serviceaccounts)
- [Webhooks](#webhooks)
- [SpeechToText](#speechtotext)
- [ForcedAlignment](#forcedalignment)
- [ConversationalAi](#conversationalai)
- [Music](#music)
- [ConversationalAi Conversations](#conversationalai-conversations)
- [ConversationalAi Twilio](#conversationalai-twilio)
- [ConversationalAi Agents](#conversationalai-agents)
- [ConversationalAi Tests](#conversationalai-tests)
- [ConversationalAi PhoneNumbers](#conversationalai-phonenumbers)
- [ConversationalAi LlmUsage](#conversationalai-llmusage)
- [ConversationalAi KnowledgeBase](#conversationalai-knowledgebase)
- [ConversationalAi Tools](#conversationalai-tools)
- [ConversationalAi Settings](#conversationalai-settings)
- [ConversationalAi Secrets](#conversationalai-secrets)
- [ConversationalAi BatchCalls](#conversationalai-batchcalls)
- [ConversationalAi SipTrunk](#conversationalai-siptrunk)
- [ConversationalAi McpServers](#conversationalai-mcpservers)
- [ConversationalAi Agents Widget](#conversationalai-agents-widget)
- [ConversationalAi Agents Link](#conversationalai-agents-link)
- [ConversationalAi Agents KnowledgeBase](#conversationalai-agents-knowledgebase)
- [ConversationalAi Agents LlmUsage](#conversationalai-agents-llmusage)
- [ConversationalAi Agents Widget Avatar](#conversationalai-agents-widget-avatar)
- [ConversationalAi Conversations Audio](#conversationalai-conversations-audio)
- [ConversationalAi Conversations Feedback](#conversationalai-conversations-feedback)
- [ConversationalAi Dashboard Settings](#conversationalai-dashboard-settings)
- [ConversationalAi KnowledgeBase Documents](#conversationalai-knowledgebase-documents)
- [ConversationalAi KnowledgeBase Document](#conversationalai-knowledgebase-document)
- [ConversationalAi KnowledgeBase Documents Chunk](#conversationalai-knowledgebase-documents-chunk)
- [ConversationalAi McpServers Tools](#conversationalai-mcpservers-tools)
- [ConversationalAi McpServers ApprovalPolicy](#conversationalai-mcpservers-approvalpolicy)
- [ConversationalAi McpServers ToolApprovals](#conversationalai-mcpservers-toolapprovals)
- [ConversationalAi McpServers ToolConfigs](#conversationalai-mcpservers-toolconfigs)
- [ConversationalAi Tests Invocations](#conversationalai-tests-invocations)
- [Dubbing Resource](#dubbing-resource)
- [Dubbing Audio](#dubbing-audio)
- [Dubbing Transcript](#dubbing-transcript)
- [Dubbing Resource Language](#dubbing-resource-language)
- [Dubbing Resource Segment](#dubbing-resource-segment)
- [Dubbing Resource Speaker](#dubbing-resource-speaker)
- [Dubbing Resource Speaker Segment](#dubbing-resource-speaker-segment)
- [Music CompositionPlan](#music-compositionplan)
- [PronunciationDictionaries Rules](#pronunciationdictionaries-rules)
- [ServiceAccounts ApiKeys](#serviceaccounts-apikeys)
- [SpeechToText Transcripts](#speechtotext-transcripts)
- [Studio Projects](#studio-projects)
- [Studio Projects PronunciationDictionaries](#studio-projects-pronunciationdictionaries)
- [Studio Projects Content](#studio-projects-content)
- [Studio Projects Snapshots](#studio-projects-snapshots)
- [Studio Projects Chapters](#studio-projects-chapters)
- [Studio Projects Chapters Snapshots](#studio-projects-chapters-snapshots)
- [TextToVoice Preview](#texttovoice-preview)
- [Tokens SingleUse](#tokens-singleuse)
- [User Subscription](#user-subscription)
- [Voices Settings](#voices-settings)
- [Voices Ivc](#voices-ivc)
- [Voices Pvc](#voices-pvc)
- [Voices Pvc Samples](#voices-pvc-samples)
- [Voices Pvc Verification](#voices-pvc-verification)
- [Voices Pvc Samples Audio](#voices-pvc-samples-audio)
- [Voices Pvc Samples Waveform](#voices-pvc-samples-waveform)
- [Voices Pvc Samples Speakers](#voices-pvc-samples-speakers)
- [Voices Pvc Samples Speakers Audio](#voices-pvc-samples-speakers-audio)
- [Voices Pvc Verification Captcha](#voices-pvc-verification-captcha)
- [Voices Samples Audio](#voices-samples-audio)
- [Workspace Groups](#workspace-groups)
- [Workspace Invites](#workspace-invites)
- [Workspace Members](#workspace-members)
- [Workspace Resources](#workspace-resources)
- [Workspace Groups Members](#workspace-groups-members)

client.save_a_voice_preview()

#### 📝 Description

Add a generated voice to the voice library.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.save_a_voice_preview()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## History
client.history.list(...)

#### 📝 Description

Returns a list of your generated audio.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.list(
    page_size=1,
    start_after_history_item_id="start_after_history_item_id",
    voice_id="voice_id",
    model_id="model_id",
    date_before_unix=1,
    date_after_unix=1,
    sort_direction="asc",
    search="search",
    source="TTS",
)

```

#### ⚙️ Parameters

**page_size:** `typing.Optional[int]` — How many history items to return at maximum. Can not exceed 1000, defaults to 100.


**start_after_history_item_id:** `typing.Optional[str]` — After which ID to start fetching, use this parameter to paginate across a large collection of history items. In case this parameter is not provided history items will be fetched starting from the most recently created one ordered descending by their creation date.


**voice_id:** `typing.Optional[str]` — ID of the voice to be filtered for. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**model_id:** `typing.Optional[str]` — Search term used for filtering history items. If provided, source becomes required.


**date_before_unix:** `typing.Optional[int]` — Unix timestamp to filter history items before this date (exclusive).


**date_after_unix:** `typing.Optional[int]` — Unix timestamp to filter history items after this date (inclusive).


**sort_direction:** `typing.Optional[HistoryListRequestSortDirection]` — Sort direction for the results.


**search:** `typing.Optional[str]` — search term used for filtering


**source:** `typing.Optional[HistoryListRequestSource]` — Source of the generated history item


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.history.get(...)

#### 📝 Description

Retrieves a history item.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.get(
    history_item_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**history_item_id:** `str` — ID of the history item to be used. You can use the [Get generated items](/docs/api-reference/history/get-all) endpoint to retrieve a list of history items.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.history.delete(...)

#### 📝 Description

Delete a history item by its ID

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.delete(
    history_item_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**history_item_id:** `str` — ID of the history item to be used. You can use the [Get generated items](/docs/api-reference/history/get-all) endpoint to retrieve a list of history items.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.history.get_audio(...)

#### 📝 Description

Returns the audio of an history item.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.get_audio(
    history_item_id="history_item_id",
)

```

#### ⚙️ Parameters

**history_item_id:** `str` — ID of the history item to be used. You can use the [Get generated items](/docs/api-reference/history/get-all) endpoint to retrieve a list of history items.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.history.download(...)

#### 📝 Description

Download one or more history items. If one history item ID is provided, we will return a single audio file. If more than one history item IDs are provided, we will provide the history items packed into a .zip file.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.history.download(
    history_item_ids=["history_item_ids", "history_item_ids"],
)

```

#### ⚙️ Parameters

**history_item_ids:** `typing.Sequence[str]` — A list of history items to download, you can get IDs of history items and other metadata using the GET https://api.elevenlabs.io/v1/history endpoint.


**output_format:** `typing.Optional[str]` — Output format to transcode the audio file, can be wav or default.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## TextToSoundEffects
client.text_to_sound_effects.convert(...)

#### 📝 Description

Turn text into sound effects for your videos, voice-overs or video games using the most advanced sound effects models in the world.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_sound_effects.convert(
    text="Spacious braam suitable for high-impact movie trailer moments",
)

```

#### ⚙️ Parameters

**text:** `str` — The text that will get converted into a sound effect.


**output_format:** `typing.Optional[TextToSoundEffectsConvertRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**loop:** `typing.Optional[bool]` — Whether to create a sound effect that loops smoothly. Only available for the 'eleven_text_to_sound_v2 model'.


**duration_seconds:** `typing.Optional[float]` — The duration of the sound which will be generated in seconds. Must be at least 0.5 and at most 30. If set to None we will guess the optimal duration using the prompt. Defaults to None.


**prompt_influence:** `typing.Optional[float]` — A higher prompt influence makes your generation follow the prompt more closely while also making generations less variable. Must be a value between 0 and 1. Defaults to 0.3.


**model_id:** `typing.Optional[str]` — The model ID to use for the sound generation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## AudioIsolation
## Samples
client.samples.delete(...)

#### 📝 Description

Removes a sample by its ID.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.samples.delete(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**sample_id:** `str` — ID of the sample to be used. You can use the [Get voices](/docs/api-reference/voices/get) endpoint list all the available samples for a voice.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## TextToSpeech
client.text_to_speech.convert(...)

#### 📝 Description

Converts text into speech using a voice of your choice and returns audio.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_speech.convert(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    text="The first move is what sets everything in motion.",
    model_id="eleven_multilingual_v2",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**text:** `str` — The text that will get converted into speech.


**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.


**optimize_streaming_latency:** `typing.Optional[int]`

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.


**output_format:** `typing.Optional[TextToSpeechConvertRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.


**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.


**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request.


**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.


**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.


**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the speech's continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.


**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that come after this generation. next_request_ids is especially useful for maintaining the speech's continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next_request_id (and that of clip 1 as a previous_request_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.


**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.


**apply_text_normalization:** `typing.Optional[BodyTextToSpeechFullApplyTextNormalization]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. For 'eleven_turbo_v2_5' and 'eleven_flash_v2_5' models, text normalization can only be enabled with Enterprise plans.


**apply_language_text_normalization:** `typing.Optional[bool]` — This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.text_to_speech.convert_with_timestamps(...)

#### 📝 Description

Generate speech from text with precise character-level timing information for audio-text synchronization.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_speech.convert_with_timestamps(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    enable_logging=True,
    optimize_streaming_latency=1,
    output_format="mp3_22050_32",
    text="This is a test for the API of ElevenLabs.",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**text:** `str` — The text that will get converted into speech.


**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.


**optimize_streaming_latency:** `typing.Optional[int]`

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.


**output_format:** `typing.Optional[TextToSpeechConvertWithTimestampsRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.


**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.


**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request.


**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.


**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.


**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the speech's continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.


**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that come after this generation. next_request_ids is especially useful for maintaining the speech's continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next_request_id (and that of clip 1 as a previous_request_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.


**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.


**apply_text_normalization:** `typing.Optional[BodyTextToSpeechFullWithTimestampsApplyTextNormalization]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. For 'eleven_turbo_v2_5' and 'eleven_flash_v2_5' models, text normalization can only be enabled with Enterprise plans.


**apply_language_text_normalization:** `typing.Optional[bool]` — This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.text_to_speech.stream(...)

#### 📝 Description

Converts text into speech using a voice of your choice and returns audio as an audio stream.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_speech.stream(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    text="The first move is what sets everything in motion.",
    model_id="eleven_multilingual_v2",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**text:** `str` — The text that will get converted into speech.


**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.


**optimize_streaming_latency:** `typing.Optional[int]`

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.


**output_format:** `typing.Optional[TextToSpeechStreamRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.


**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.


**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request.


**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.


**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.


**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the speech's continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.


**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that come after this generation. next_request_ids is especially useful for maintaining the speech's continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next_request_id (and that of clip 1 as a previous_request_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.


**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.


**apply_text_normalization:** `typing.Optional[BodyTextToSpeechStreamApplyTextNormalization]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. For 'eleven_turbo_v2_5' and 'eleven_flash_v2_5' models, text normalization can only be enabled with Enterprise plans.


**apply_language_text_normalization:** `typing.Optional[bool]` — This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.text_to_speech.stream_with_timestamps(...)

#### 📝 Description

Converts text into speech using a voice of your choice and returns a stream of JSONs containing audio as a base64 encoded string together with information on when which character was spoken.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
response = client.text_to_speech.stream_with_timestamps(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    text="The first move is what sets everything in motion.",
    model_id="eleven_multilingual_v2",
)
for chunk in response.data:
    yield chunk

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**text:** `str` — The text that will get converted into speech.


**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.


**optimize_streaming_latency:** `typing.Optional[int]`

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.


**output_format:** `typing.Optional[TextToSpeechStreamWithTimestampsRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.


**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.


**voice_settings:** `typing.Optional[VoiceSettings]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request.


**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**previous_text:** `typing.Optional[str]` — The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.


**next_text:** `typing.Optional[str]` — The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.


**previous_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that were generated before this generation. Can be used to improve the speech's continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous_text and previous_request_ids is send, previous_text will be ignored. A maximum of 3 request_ids can be send.


**next_request_ids:** `typing.Optional[typing.Sequence[str]]` — A list of request_id of the samples that come after this generation. next_request_ids is especially useful for maintaining the speech's continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next_request_id (and that of clip 1 as a previous_request_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next_text and next_request_ids is send, next_text will be ignored. A maximum of 3 request_ids can be send.


**use_pvc_as_ivc:** `typing.Optional[bool]` — If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.


**apply_text_normalization:** `typing.Optional[BodyTextToSpeechStreamWithTimestampsApplyTextNormalization]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. For 'eleven_turbo_v2_5' and 'eleven_flash_v2_5' models, text normalization can only be enabled with Enterprise plans.


**apply_language_text_normalization:** `typing.Optional[bool]` — This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## TextToDialogue
client.text_to_dialogue.convert(...)

#### 📝 Description

Converts a list of text and voice ID pairs into speech (dialogue) and returns audio.

#### 🔌 Usage

```python
from elevenlabs import DialogueInput, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_dialogue.convert(
    inputs=[
        DialogueInput(
            text="Knock knock",
            voice_id="JBFqnCBsd6RMkjVDRZzb",
        ),
        DialogueInput(
            text="Who is there?",
            voice_id="Aw4FAjKCGjjNkVhN1Xmq",
        ),
    ],
)

```

#### ⚙️ Parameters

**inputs:** `typing.Sequence[DialogueInput]` — A list of dialogue inputs, each containing text and a voice ID which will be converted into speech.


**output_format:** `typing.Optional[TextToDialogueConvertRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.


**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.


**settings:** `typing.Optional[ModelSettingsResponseModel]` — Settings controlling the dialogue generation.


**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**apply_text_normalization:** `typing.Optional[
    BodyTextToDialogueMultiVoiceV1TextToDialoguePostApplyTextNormalization
]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. For 'eleven_turbo_v2_5' and 'eleven_flash_v2_5' models, text normalization can only be enabled with Enterprise plans.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.text_to_dialogue.stream(...)

#### 📝 Description

Converts a list of text and voice ID pairs into speech (dialogue) and returns an audio stream.

#### 🔌 Usage

```python
from elevenlabs import DialogueInput, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_dialogue.stream(
    inputs=[
        DialogueInput(
            text="Knock knock",
            voice_id="JBFqnCBsd6RMkjVDRZzb",
        ),
        DialogueInput(
            text="Who is there?",
            voice_id="Aw4FAjKCGjjNkVhN1Xmq",
        ),
    ],
)

```

#### ⚙️ Parameters

**inputs:** `typing.Sequence[DialogueInput]` — A list of dialogue inputs, each containing text and a voice ID which will be converted into speech.


**output_format:** `typing.Optional[TextToDialogueStreamRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.


**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.


**settings:** `typing.Optional[ModelSettingsResponseModel]` — Settings controlling the dialogue generation.


**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**apply_text_normalization:** `typing.Optional[
    BodyTextToDialogueMultiVoiceStreamingV1TextToDialogueStreamPostApplyTextNormalization
]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. For 'eleven_turbo_v2_5' and 'eleven_flash_v2_5' models, text normalization can only be enabled with Enterprise plans.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.text_to_dialogue.stream_with_timestamps(...)

#### 📝 Description

Converts a list of text and voice ID pairs into speech (dialogue) and returns a stream of JSON blobs containing audio as a base64 encoded string and timestamps

#### 🔌 Usage

```python
from elevenlabs import DialogueInput, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
response = client.text_to_dialogue.stream_with_timestamps(
    output_format="mp3_22050_32",
    inputs=[
        DialogueInput(
            text="Hello, how are you?",
            voice_id="bYTqZQo3Jz7LQtmGTgwi",
        ),
        DialogueInput(
            text="I'm doing well, thank you!",
            voice_id="6lCwbsX1yVjD49QmpkTR",
        ),
    ],
)
for chunk in response.data:
    yield chunk

```

#### ⚙️ Parameters

**inputs:** `typing.Sequence[DialogueInput]` — A list of dialogue inputs, each containing text and a voice ID which will be converted into speech.


**output_format:** `typing.Optional[TextToDialogueStreamWithTimestampsRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.


**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.


**settings:** `typing.Optional[ModelSettingsResponseModel]` — Settings controlling the dialogue generation.


**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**apply_text_normalization:** `typing.Optional[BodyTextToDialogueStreamWithTimestampsApplyTextNormalization]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. For 'eleven_turbo_v2_5' and 'eleven_flash_v2_5' models, text normalization can only be enabled with Enterprise plans.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.text_to_dialogue.convert_with_timestamps(...)

#### 📝 Description

Generate dialogue from text with precise character-level timing information for audio-text synchronization.

#### 🔌 Usage

```python
from elevenlabs import DialogueInput, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_dialogue.convert_with_timestamps(
    output_format="mp3_22050_32",
    inputs=[
        DialogueInput(
            text="Hello, how are you?",
            voice_id="bYTqZQo3Jz7LQtmGTgwi",
        ),
        DialogueInput(
            text="I'm doing well, thank you!",
            voice_id="6lCwbsX1yVjD49QmpkTR",
        ),
    ],
)

```

#### ⚙️ Parameters

**inputs:** `typing.Sequence[DialogueInput]` — A list of dialogue inputs, each containing text and a voice ID which will be converted into speech.


**output_format:** `typing.Optional[TextToDialogueConvertWithTimestampsRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can_do_text_to_speech property.


**language_code:** `typing.Optional[str]` — Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.


**settings:** `typing.Optional[ModelSettingsResponseModel]` — Settings controlling the dialogue generation.


**pronunciation_dictionary_locators:** `typing.Optional[typing.Sequence[PronunciationDictionaryVersionLocator]]` — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**apply_text_normalization:** `typing.Optional[BodyTextToDialogueFullWithTimestampsApplyTextNormalization]` — This parameter controls text normalization with three modes: 'auto', 'on', and 'off'. When set to 'auto', the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With 'on', text normalization will always be applied, while with 'off', it will be skipped. For 'eleven_turbo_v2_5' and 'eleven_flash_v2_5' models, text normalization can only be enabled with Enterprise plans.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## SpeechToSpeech
client.speech_to_speech.convert(...)

#### 📝 Description

Transform audio from one voice to another. Maintain full control over emotion, timing and delivery.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.speech_to_speech.convert(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    model_id="eleven_multilingual_sts_v2",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**audio:** `from __future__ import annotations

core.File` — See core.File for more documentation


**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.


**optimize_streaming_latency:** `typing.Optional[int]`

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.


**output_format:** `typing.Optional[SpeechToSpeechConvertRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for speech to speech, you can check this using the can_do_voice_conversion property.


**voice_settings:** `typing.Optional[str]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request. Needs to be send as a JSON encoded string.


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**remove_background_noise:** `typing.Optional[bool]` — If set, will remove the background noise from your audio input using our audio isolation model. Only applies to Voice Changer.


**file_format:** `typing.Optional[SpeechToSpeechConvertRequestFileFormat]` — The format of input audio. Options are 'pcm_s16le_16' or 'other' For `pcm_s16le_16`, the input audio must be 16-bit PCM at a 16kHz sample rate, single channel (mono), and little-endian byte order. Latency will be lower than with passing an encoded waveform.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.speech_to_speech.stream(...)

#### 📝 Description

Stream audio from one voice to another. Maintain full control over emotion, timing and delivery.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.speech_to_speech.stream(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    model_id="eleven_multilingual_sts_v2",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. Use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**audio:** `from __future__ import annotations

core.File` — See core.File for more documentation


**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.


**optimize_streaming_latency:** `typing.Optional[int]`

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.


**output_format:** `typing.Optional[SpeechToSpeechStreamRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[str]` — Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for speech to speech, you can check this using the can_do_voice_conversion property.


**voice_settings:** `typing.Optional[str]` — Voice settings overriding stored settings for the given voice. They are applied only on the given request. Needs to be send as a JSON encoded string.


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.


**remove_background_noise:** `typing.Optional[bool]` — If set, will remove the background noise from your audio input using our audio isolation model. Only applies to Voice Changer.


**file_format:** `typing.Optional[SpeechToSpeechStreamRequestFileFormat]` — The format of input audio. Options are 'pcm_s16le_16' or 'other' For `pcm_s16le_16`, the input audio must be 16-bit PCM at a 16kHz sample rate, single channel (mono), and little-endian byte order. Latency will be lower than with passing an encoded waveform.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## TextToVoice
client.text_to_voice.create_previews(...)

#### 📝 Description

Create a voice from a text prompt.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_voice.create_previews(
    output_format="mp3_22050_32",
    voice_description="A sassy squeaky mouse",
)

```

#### ⚙️ Parameters

**voice_description:** `str` — Description to use for the created voice.


**output_format:** `typing.Optional[TextToVoiceCreatePreviewsRequestOutputFormat]` — The output format of the generated audio.


**text:** `typing.Optional[str]` — Text to generate, text length has to be between 100 and 1000.


**auto_generate_text:** `typing.Optional[bool]` — Whether to automatically generate a text suitable for the voice description.


**loudness:** `typing.Optional[float]` — Controls the volume level of the generated voice. -1 is quietest, 1 is loudest, 0 corresponds to roughly -24 LUFS.


**quality:** `typing.Optional[float]` — Higher quality results in better voice output but less variety.


**seed:** `typing.Optional[int]` — Random number that controls the voice generation. Same seed with same inputs produces same voice.


**guidance_scale:** `typing.Optional[float]` — Controls how closely the AI follows the prompt. Lower numbers give the AI more freedom to be creative, while higher numbers force it to stick more to the prompt. High numbers can cause voice to sound artificial or robotic. We recommend to use longer, more detailed prompts at lower Guidance Scale.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.text_to_voice.create(...)

#### 📝 Description

Create a voice from previously generated voice preview. This endpoint should be called after you fetched a generated_voice_id using POST /v1/text-to-voice/design or POST /v1/text-to-voice/:voice_id/remix.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_voice.create(
    voice_name="Sassy squeaky mouse",
    voice_description="A sassy squeaky mouse",
    generated_voice_id="37HceQefKmEi3bGovXjL",
)

```

#### ⚙️ Parameters

**voice_name:** `str` — Name to use for the created voice.


**voice_description:** `str` — Description to use for the created voice.


**generated_voice_id:** `str` — The generated_voice_id to create, call POST /v1/text-to-voice/create-previews and fetch the generated_voice_id from the response header if don't have one yet.


**labels:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]` — Optional, metadata to add to the created voice. Defaults to None.


**played_not_selected_voice_ids:** `typing.Optional[typing.Sequence[str]]` — List of voice ids that the user has played but not selected. Used for RLHF.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.text_to_voice.design(...)

#### 📝 Description

Design a voice via a prompt. This method returns a list of voice previews. Each preview has a generated_voice_id and a sample of the voice as base64 encoded mp3 audio. To create a voice use the generated_voice_id of the preferred preview with the /v1/text-to-voice endpoint.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_voice.design(
    output_format="mp3_22050_32",
    voice_description="A sassy squeaky mouse",
)

```

#### ⚙️ Parameters

**voice_description:** `str` — Description to use for the created voice.


**output_format:** `typing.Optional[TextToVoiceDesignRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**model_id:** `typing.Optional[VoiceDesignRequestModelModelId]` — Model to use for the voice generation. Possible values: eleven_multilingual_ttv_v2, eleven_ttv_v3.


**text:** `typing.Optional[str]` — Text to generate, text length has to be between 100 and 1000.


**auto_generate_text:** `typing.Optional[bool]` — Whether to automatically generate a text suitable for the voice description.


**loudness:** `typing.Optional[float]` — Controls the volume level of the generated voice. -1 is quietest, 1 is loudest, 0 corresponds to roughly -24 LUFS.


**seed:** `typing.Optional[int]` — Random number that controls the voice generation. Same seed with same inputs produces same voice.


**guidance_scale:** `typing.Optional[float]` — Controls how closely the AI follows the prompt. Lower numbers give the AI more freedom to be creative, while higher numbers force it to stick more to the prompt. High numbers can cause voice to sound artificial or robotic. We recommend to use longer, more detailed prompts at lower Guidance Scale.


**stream_previews:** `typing.Optional[bool]` — Determines whether the Text to Voice previews should be included in the response. If true, only the generated IDs will be returned which can then be streamed via the /v1/text-to-voice/:generated_voice_id/stream endpoint.


**remixing_session_id:** `typing.Optional[str]` — The remixing session id.


**remixing_session_iteration_id:** `typing.Optional[str]` — The id of the remixing session iteration where these generations should be attached to. If not provided, a new iteration will be created.


**quality:** `typing.Optional[float]` — Higher quality results in better voice output but less variety.


**reference_audio_base_64:** `typing.Optional[str]` — Reference audio to use for the voice generation. The audio should be base64 encoded. Only supported when using the  eleven_ttv_v3 model.


**prompt_strength:** `typing.Optional[float]` — Controls the balance of prompt versus reference audio when generating voice samples. 0 means almost no prompt influence, 1 means almost no reference audio influence. Only supported when using the eleven_ttv_v3 model and providing reference audio.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.text_to_voice.remix(...)

#### 📝 Description

Remix an existing voice via a prompt. This method returns a list of voice previews. Each preview has a generated_voice_id and a sample of the voice as base64 encoded mp3 audio. To create a voice use the generated_voice_id of the preferred preview with the /v1/text-to-voice endpoint.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_voice.remix(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    output_format="mp3_22050_32",
    voice_description="Make the voice have a higher pitch.",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**voice_description:** `str` — Description of the changes to make to the voice.


**output_format:** `typing.Optional[TextToVoiceRemixRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**text:** `typing.Optional[str]` — Text to generate, text length has to be between 100 and 1000.


**auto_generate_text:** `typing.Optional[bool]` — Whether to automatically generate a text suitable for the voice description.


**loudness:** `typing.Optional[float]` — Controls the volume level of the generated voice. -1 is quietest, 1 is loudest, 0 corresponds to roughly -24 LUFS.


**seed:** `typing.Optional[int]` — Random number that controls the voice generation. Same seed with same inputs produces same voice.


**guidance_scale:** `typing.Optional[float]` — Controls how closely the AI follows the prompt. Lower numbers give the AI more freedom to be creative, while higher numbers force it to stick more to the prompt. High numbers can cause voice to sound artificial or robotic. We recommend to use longer, more detailed prompts at lower Guidance Scale.


**stream_previews:** `typing.Optional[bool]` — Determines whether the Text to Voice previews should be included in the response. If true, only the generated IDs will be returned which can then be streamed via the /v1/text-to-voice/:generated_voice_id/stream endpoint.


**remixing_session_id:** `typing.Optional[str]` — The remixing session id.


**remixing_session_iteration_id:** `typing.Optional[str]` — The id of the remixing session iteration where these generations should be attached to. If not provided, a new iteration will be created.


**prompt_strength:** `typing.Optional[float]` — Controls the balance of prompt versus reference audio when generating voice samples. 0 means almost no prompt influence, 1 means almost no reference audio influence. Only supported when using the eleven_ttv_v3 model and providing reference audio.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## user
client.user.get()

#### 📝 Description

Gets information about the user

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.user.get()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices
client.voices.get_all(...)

#### 📝 Description

Returns a list of all available voices for a user.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_all(
    show_legacy=True,
)

```

#### ⚙️ Parameters

**show_legacy:** `typing.Optional[bool]` — If set to true, legacy premade voices will be included in responses from /v1/voices


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.search(...)

#### 📝 Description

Gets a list of all available voices for a user with search, filtering and pagination.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.search(
    next_page_token="next_page_token",
    page_size=1,
    search="search",
    sort="sort",
    sort_direction="sort_direction",
    voice_type="voice_type",
    category="category",
    fine_tuning_state="fine_tuning_state",
    collection_id="collection_id",
    include_total_count=True,
)

```

#### ⚙️ Parameters

**next_page_token:** `typing.Optional[str]` — The next page token to use for pagination. Returned from the previous request.


**page_size:** `typing.Optional[int]` — How many voices to return at maximum. Can not exceed 100, defaults to 10. Page 0 may include more voices due to default voices being included.


**search:** `typing.Optional[str]` — Search term to filter voices by. Searches in name, description, labels, category.


**sort:** `typing.Optional[str]` — Which field to sort by, one of 'created_at_unix' or 'name'. 'created_at_unix' may not be available for older voices.


**sort_direction:** `typing.Optional[str]` — Which direction to sort the voices in. 'asc' or 'desc'.


**voice_type:** `typing.Optional[str]` — Type of the voice to filter by. One of 'personal', 'community', 'default', 'workspace', 'non-default'. 'non-default' is equal to all but 'default'.


**category:** `typing.Optional[str]` — Category of the voice to filter by. One of 'premade', 'cloned', 'generated', 'professional'


**fine_tuning_state:** `typing.Optional[str]` — State of the voice's fine tuning to filter by. Applicable only to professional voices clones. One of 'draft', 'not_verified', 'not_started', 'queued', 'fine_tuning', 'fine_tuned', 'failed', 'delayed'


**collection_id:** `typing.Optional[str]` — Collection ID to filter voices by.


**include_total_count:** `typing.Optional[bool]` — Whether to include the total count of voices found in the response. Incurs a performance cost.


**voice_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Voice IDs to lookup by. Maximum 100 voice IDs.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.get(...)

#### 📝 Description

Returns metadata about a specific voice.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    with_settings=True,
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**with_settings:** `typing.Optional[bool]` — This parameter is now deprecated. It is ignored and will be removed in a future version.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.delete(...)

#### 📝 Description

Deletes a voice by its ID.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.delete(
    voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.update(...)

#### 📝 Description

Edit a voice created by you.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.update(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    name="name",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**name:** `str` — The name that identifies this voice. This will be displayed in the dropdown of the website.


**files:** `from __future__ import annotations

typing.Optional[typing.List[core.File]]` — See core.File for more documentation


**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.


**description:** `typing.Optional[str]` — A description of the voice.


**labels:** `typing.Optional[str]` — Serialized labels dictionary for the voice.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.share(...)

#### 📝 Description

Add a shared voice to your collection of Voices

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.share(
    public_user_id="63e06b7e7cafdc46be4d2e0b3f045940231ae058d508589653d74d1265a574ca",
    voice_id="21m00Tcm4TlvDq8ikWAM",
    new_name="John Smith",
)

```

#### ⚙️ Parameters

**public_user_id:** `str` — Public user ID used to publicly identify ElevenLabs users.


**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**new_name:** `str` — The name that identifies this voice. This will be displayed in the dropdown of the website.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.get_shared(...)

#### 📝 Description

Retrieves a list of shared voices.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.get_shared(
    page_size=1,
    category="professional",
    gender="gender",
    age="age",
    accent="accent",
    language="language",
    locale="locale",
    search="search",
    featured=True,
    min_notice_period_days=1,
    include_custom_rates=True,
    include_live_moderated=True,
    reader_app_enabled=True,
    owner_id="owner_id",
    sort="sort",
    page=1,
)

```

#### ⚙️ Parameters

**page_size:** `typing.Optional[int]` — How many shared voices to return at maximum. Can not exceed 100, defaults to 30.


**category:** `typing.Optional[VoicesGetSharedRequestCategory]` — Voice category used for filtering


**gender:** `typing.Optional[str]` — Gender used for filtering


**age:** `typing.Optional[str]` — Age used for filtering


**accent:** `typing.Optional[str]` — Accent used for filtering


**language:** `typing.Optional[str]` — Language used for filtering


**locale:** `typing.Optional[str]` — Locale used for filtering


**search:** `typing.Optional[str]` — Search term used for filtering


**use_cases:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Use-case used for filtering


**descriptives:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Search term used for filtering


**featured:** `typing.Optional[bool]` — Filter featured voices


**min_notice_period_days:** `typing.Optional[int]` — Filter voices with a minimum notice period of the given number of days.


**include_custom_rates:** `typing.Optional[bool]` — Include/exclude voices with custom rates


**include_live_moderated:** `typing.Optional[bool]` — Include/exclude voices that are live moderated


**reader_app_enabled:** `typing.Optional[bool]` — Filter voices that are enabled for the reader app


**owner_id:** `typing.Optional[str]` — Filter voices by public owner ID


**sort:** `typing.Optional[str]` — Sort criteria


**page:** `typing.Optional[int]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.find_similar_voices(...)

#### 📝 Description

Returns a list of shared voices similar to the provided audio sample. If neither similarity_threshold nor top_k is provided, we will apply default values.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.find_similar_voices()

```

#### ⚙️ Parameters

**audio_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**similarity_threshold:** `typing.Optional[float]` — Threshold for voice similarity between provided sample and library voices. Values range from 0 to 2. The smaller the value the more similar voices will be returned.


**top_k:** `typing.Optional[int]` — Number of most similar voices to return. If similarity_threshold is provided, less than this number of voices may be returned. Values range from 1 to 100.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Studio
client.studio.create_podcast(...)

#### 📝 Description

Create and auto-convert a podcast project. Currently, the LLM cost is covered by us but you will still be charged for the audio generation. In the future, you will be charged for both the LLM and audio generation costs.

#### 🔌 Usage

```python
from elevenlabs import (
    ElevenLabs,
    PodcastConversationModeData,
    PodcastTextSource,
)
from elevenlabs.studio import (
    BodyCreatePodcastV1StudioPodcastsPostMode_Conversation,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.create_podcast(
    safety_identifier="safety-identifier",
    model_id="eleven_multilingual_v2",
    mode=BodyCreatePodcastV1StudioPodcastsPostMode_Conversation(
        conversation=PodcastConversationModeData(
            host_voice_id="aw1NgEzBg83R7vgmiJt6",
            guest_voice_id="aw1NgEzBg83R7vgmiJt7",
        ),
    ),
    source=PodcastTextSource(
        text="This is a test podcast.",
    ),
)

```

#### ⚙️ Parameters

**model_id:** `str` — The ID of the model to be used for this Studio project, you can query GET /v1/models to list all available models.


**mode:** `BodyCreatePodcastV1StudioPodcastsPostMode` — The type of podcast to generate. Can be 'conversation', an interaction between two voices, or 'bulletin', a monologue.


**source:** `BodyCreatePodcastV1StudioPodcastsPostSource` — The source content for the Podcast.


**safety_identifier:** `typing.Optional[str]` — Used for moderation. Your workspace must be allowlisted to use this feature.


**quality_preset:** `typing.Optional[BodyCreatePodcastV1StudioPodcastsPostQualityPreset]`

Output quality of the generated audio. Must be one of:
standard - standard output format, 128kbps with 44.1kHz sample rate.
high - high quality output format, 192kbps with 44.1kHz sample rate and major improvements on our side. Using this setting increases the credit cost by 20%.
ultra - ultra quality output format, 192kbps with 44.1kHz sample rate and highest improvements on our side. Using this setting increases the credit cost by 50%.
ultra lossless - ultra quality output format, 705.6kbps with 44.1kHz sample rate and highest improvements on our side in a fully lossless format. Using this setting increases the credit cost by 100%.


**duration_scale:** `typing.Optional[BodyCreatePodcastV1StudioPodcastsPostDurationScale]`

Duration of the generated podcast. Must be one of:
short - produces podcasts shorter than 3 minutes.
default - produces podcasts roughly between 3-7 minutes.
long - produces podcasts longer than 7 minutes.


**language:** `typing.Optional[str]` — An optional language of the Studio project. Two-letter language code (ISO 639-1).


**intro:** `typing.Optional[str]` — The intro text that will always be added to the beginning of the podcast.


**outro:** `typing.Optional[str]` — The outro text that will always be added to the end of the podcast.


**instructions_prompt:** `typing.Optional[str]` — Additional instructions prompt for the podcast generation used to adjust the podcast's style and tone.


**highlights:** `typing.Optional[typing.Sequence[str]]` — A brief summary or highlights of the Studio project's content, providing key points or themes. This should be between 10 and 70 characters.


**callback_url:** `typing.Optional[str]`

    A url that will be called by our service when the Studio project is converted. Request will contain a json blob containing the status of the conversion
    Messages:
    1. When project was converted successfully:
    {
      type: "project_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        conversion_status: "success",
        project_snapshot_id: "22m00Tcm4TlvDq8ikMAT",
        error_details: None,
      }
    }
    2. When project conversion failed:
    {
      type: "project_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        conversion_status: "error",
        project_snapshot_id: None,
        error_details: "Error details if conversion failed"
      }
    }

    3. When chapter was converted successfully:
    {
      type: "chapter_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        chapter_id: "22m00Tcm4TlvDq8ikMAT",
        conversion_status: "success",
        chapter_snapshot_id: "23m00Tcm4TlvDq8ikMAV",
        error_details: None,
      }
    }
    4. When chapter conversion failed:
    {
      type: "chapter_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        chapter_id: "22m00Tcm4TlvDq8ikMAT",
        conversion_status: "error",
        chapter_snapshot_id: None,
        error_details: "Error details if conversion failed"
      }
    }



**apply_text_normalization:** `typing.Optional[BodyCreatePodcastV1StudioPodcastsPostApplyTextNormalization]`

    This parameter controls text normalization with four modes: 'auto', 'on', 'apply_english' and 'off'.
    When set to 'auto', the system will automatically decide whether to apply text normalization
    (e.g., spelling out numbers). With 'on', text normalization will always be applied, while
    with 'off', it will be skipped. 'apply_english' is the same as 'on' but will assume that text is in English.



**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Dubbing
client.dubbing.list(...)

#### 📝 Description

List the dubs you have access to.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.list(
    cursor="cursor",
    page_size=1,
    dubbing_status="dubbing",
    filter_by_creator="personal",
    order_direction="DESCENDING",
)

```

#### ⚙️ Parameters

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**page_size:** `typing.Optional[int]` — How many dubs to return at maximum. Can not exceed 200, defaults to 100.


**dubbing_status:** `typing.Optional[DubbingListRequestDubbingStatus]` — What state the dub is currently in.


**filter_by_creator:** `typing.Optional[DubbingListRequestFilterByCreator]` — Filters who created the resources being listed, whether it was the user running the request or someone else that shared the resource with them.


**order_by:** `typing.Optional[typing.Literal["created_at"]]` — The field to use for ordering results from this query.


**order_direction:** `typing.Optional[DubbingListRequestOrderDirection]` — The order direction to use for results from this query.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.create(...)

#### 📝 Description

Dubs a provided audio or video file into given language.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.create()

```

#### ⚙️ Parameters

**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**csv_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**foreground_audio_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**background_audio_file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**name:** `typing.Optional[str]` — Name of the dubbing project.


**source_url:** `typing.Optional[str]` — URL of the source video/audio file.


**source_lang:** `typing.Optional[str]` — Source language.


**target_lang:** `typing.Optional[str]` — The Target language to dub the content into.


**target_accent:** `typing.Optional[str]` — [Experimental] An accent to apply when selecting voices from the library and to use to inform translation of the dialect to prefer.


**num_speakers:** `typing.Optional[int]` — Number of speakers to use for the dubbing. Set to 0 to automatically detect the number of speakers


**watermark:** `typing.Optional[bool]` — Whether to apply watermark to the output video.


**start_time:** `typing.Optional[int]` — Start time of the source video/audio file.


**end_time:** `typing.Optional[int]` — End time of the source video/audio file.


**highest_resolution:** `typing.Optional[bool]` — Whether to use the highest resolution available.


**drop_background_audio:** `typing.Optional[bool]` — An advanced setting. Whether to drop background audio from the final dub. This can improve dub quality where it's known that audio shouldn't have a background track such as for speeches or monologues.


**use_profanity_filter:** `typing.Optional[bool]` — [BETA] Whether transcripts should have profanities censored with the words '[censored]'


**dubbing_studio:** `typing.Optional[bool]` — Whether to prepare dub for edits in dubbing studio or edits as a dubbing resource.


**disable_voice_cloning:** `typing.Optional[bool]` — Instead of using a voice clone in dubbing, use a similar voice from the ElevenLabs Voice Library. Voices used from the library will contribute towards a workspace's custom voices limit, and if there aren't enough available slots the dub will fail. Using this feature requires the caller to have the 'add_voice_from_voice_library' permission on their workspace to access new voices.


**mode:** `typing.Optional[DubbingCreateRequestMode]` — The mode in which to run this Dubbing job. Defaults to automatic, use manual if specifically providing a CSV transcript to use.


**csv_fps:** `typing.Optional[float]` — Frames per second to use when parsing a CSV file for dubbing. If not provided, FPS will be inferred from timecodes.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.get(...)

#### 📝 Description

Returns metadata about a dubbing project, including whether it's still in progress or not

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.get(
    dubbing_id="dubbing_id",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.delete(...)

#### 📝 Description

Deletes a dubbing project.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.delete(
    dubbing_id="dubbing_id",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Models
client.models.list()

#### 📝 Description

Gets a list of available models.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.models.list()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## AudioNative
client.audio_native.create(...)

#### 📝 Description

Creates Audio Native enabled project, optionally starts conversion and returns project ID and embeddable HTML snippet.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.audio_native.create(
    name="name",
)

```

#### ⚙️ Parameters

**name:** `str` — Project name.


**image:** `typing.Optional[str]` — (Deprecated) Image URL used in the player. If not provided, default image set in the Player settings is used.


**author:** `typing.Optional[str]` — Author used in the player and inserted at the start of the uploaded article. If not provided, the default author set in the Player settings is used.


**title:** `typing.Optional[str]` — Title used in the player and inserted at the top of the uploaded article. If not provided, the default title set in the Player settings is used.


**small:** `typing.Optional[bool]` — (Deprecated) Whether to use small player or not. If not provided, default value set in the Player settings is used.


**text_color:** `typing.Optional[str]` — Text color used in the player. If not provided, default text color set in the Player settings is used.


**background_color:** `typing.Optional[str]` — Background color used in the player. If not provided, default background color set in the Player settings is used.


**sessionization:** `typing.Optional[int]` — (Deprecated) Specifies for how many minutes to persist the session across page reloads. If not provided, default sessionization set in the Player settings is used.


**voice_id:** `typing.Optional[str]` — Voice ID used to voice the content. If not provided, default voice ID set in the Player settings is used.


**model_id:** `typing.Optional[str]` — TTS Model ID used in the player. If not provided, default model ID set in the Player settings is used.


**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the project to audio or not.


**apply_text_normalization:** `typing.Optional[AudioNativeCreateRequestApplyTextNormalization]`

    This parameter controls text normalization with four modes: 'auto', 'on', 'apply_english' and 'off'.
    When set to 'auto', the system will automatically decide whether to apply text normalization
    (e.g., spelling out numbers). With 'on', text normalization will always be applied, while
    with 'off', it will be skipped. 'apply_english' is the same as 'on' but will assume that text is in English.



**pronunciation_dictionary_locators:** `typing.Optional[typing.List[str]]` — A list of pronunciation dictionary locators (pronunciation_dictionary_id, version_id) encoded as a list of JSON strings for pronunciation dictionaries to be applied to the text. A list of json encoded strings is required as adding projects may occur through formData as opposed to jsonBody. To specify multiple dictionaries use multiple --form lines in your curl, such as --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"Vmd4Zor6fplcA7WrINey\",\"version_id\":\"hRPaxjlTdR7wFMhV4w0b\"}"' --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"JzWtcGQMJ6bnlWwyMo7e\",\"version_id\":\"lbmwxiLu4q6txYxgdZqn\"}"'.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.audio_native.get_settings(...)

#### 📝 Description

Get player settings for the specific project.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.audio_native.get_settings(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the Studio project.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.audio_native.update(...)

#### 📝 Description

Updates content for the specific AudioNative Project.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.audio_native.update(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the project to audio or not.


**auto_publish:** `typing.Optional[bool]` — Whether to auto publish the new project snapshot after it's converted.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## usage
client.usage.get(...)

#### 📝 Description

Returns the usage metrics for the current user or the entire workspace they are part of. The response provides a time axis based on the specified aggregation interval (default: day), with usage values for each interval along that axis. Usage is broken down by the selected breakdown type. For example, breakdown type "voice" will return the usage of each voice for each interval along the time axis.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.usage.get(
    start_unix=1,
    end_unix=1,
    include_workspace_metrics=True,
    breakdown_type="none",
    aggregation_interval="hour",
    aggregation_bucket_size=1,
    metric="credits",
)

```

#### ⚙️ Parameters

**start_unix:** `int` — UTC Unix timestamp for the start of the usage window, in milliseconds. To include the first day of the window, the timestamp should be at 00:00:00 of that day.


**end_unix:** `int` — UTC Unix timestamp for the end of the usage window, in milliseconds. To include the last day of the window, the timestamp should be at 23:59:59 of that day.


**include_workspace_metrics:** `typing.Optional[bool]` — Whether or not to include the statistics of the entire workspace.


**breakdown_type:** `typing.Optional[BreakdownTypes]` — How to break down the information. Cannot be "user" if include_workspace_metrics is False.


**aggregation_interval:** `typing.Optional[UsageAggregationInterval]` — How to aggregate usage data over time. Can be "hour", "day", "week", "month", or "cumulative".


**aggregation_bucket_size:** `typing.Optional[int]` — Aggregation bucket size in seconds. Overrides the aggregation interval.


**metric:** `typing.Optional[MetricType]` — Which metric to aggregate.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## PronunciationDictionaries
client.pronunciation_dictionaries.create_from_file(...)

#### 📝 Description

Creates a new pronunciation dictionary from a lexicon .PLS file

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.create_from_file(
    name="name",
)

```

#### ⚙️ Parameters

**name:** `str` — The name of the pronunciation dictionary, used for identification only.


**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**description:** `typing.Optional[str]` — A description of the pronunciation dictionary, used for identification only.


**workspace_access:** `typing.Optional[PronunciationDictionariesCreateFromFileRequestWorkspaceAccess]` — Should be one of 'admin', 'editor' or 'viewer'. If not provided, defaults to no access.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.pronunciation_dictionaries.create_from_rules(...)

#### 📝 Description

Creates a new pronunciation dictionary from provided rules.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs
from elevenlabs.pronunciation_dictionaries import (
    BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostRulesItem_Alias,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.create_from_rules(
    rules=[
        BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostRulesItem_Alias(
            string_to_replace="Thailand",
            alias="tie-land",
        )
    ],
    name="My Dictionary",
)

```

#### ⚙️ Parameters

**rules:** `typing.Sequence[
    BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostRulesItem
]`

List of pronunciation rules. Rule can be either:
    an alias rule: {'string_to_replace': 'a', 'type': 'alias', 'alias': 'b', }
    or a phoneme rule: {'string_to_replace': 'a', 'type': 'phoneme', 'phoneme': 'b', 'alphabet': 'ipa' }


**name:** `str` — The name of the pronunciation dictionary, used for identification only.


**description:** `typing.Optional[str]` — A description of the pronunciation dictionary, used for identification only.


**workspace_access:** `typing.Optional[
    BodyAddAPronunciationDictionaryV1PronunciationDictionariesAddFromRulesPostWorkspaceAccess
]` — Should be one of 'admin', 'editor' or 'viewer'. If not provided, defaults to no access.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.pronunciation_dictionaries.get(...)

#### 📝 Description

Get metadata for a pronunciation dictionary

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.get(
    pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**pronunciation_dictionary_id:** `str` — The id of the pronunciation dictionary


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.pronunciation_dictionaries.update(...)

#### 📝 Description

Partially update the pronunciation dictionary without changing the version

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.update(
    pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**pronunciation_dictionary_id:** `str` — The id of the pronunciation dictionary


**archived:** `typing.Optional[bool]` — The name of the pronunciation dictionary, used for identification only.


**name:** `typing.Optional[str]` — The name of the pronunciation dictionary, used for identification only.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.pronunciation_dictionaries.download(...)

#### 📝 Description

Get a PLS file with a pronunciation dictionary version rules

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.download(
    dictionary_id="dictionary_id",
    version_id="version_id",
)

```

#### ⚙️ Parameters

**dictionary_id:** `str` — The id of the pronunciation dictionary


**version_id:** `str` — The id of the pronunciation dictionary version


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.pronunciation_dictionaries.list(...)

#### 📝 Description

Get a list of the pronunciation dictionaries you have access to and their metadata

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.list(
    cursor="cursor",
    page_size=1,
    sort="creation_time_unix",
    sort_direction="sort_direction",
)

```

#### ⚙️ Parameters

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**page_size:** `typing.Optional[int]` — How many pronunciation dictionaries to return at maximum. Can not exceed 100, defaults to 30.


**sort:** `typing.Optional[PronunciationDictionariesListRequestSort]` — Which field to sort by, one of 'created_at_unix' or 'name'.


**sort_direction:** `typing.Optional[str]` — Which direction to sort the voices in. 'ascending' or 'descending'.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ServiceAccounts
client.service_accounts.list()

#### 📝 Description

List all service accounts in the workspace

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.service_accounts.list()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Webhooks
client.webhooks.list(...)

#### 📝 Description

List all webhooks for a workspace

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.webhooks.list(
    include_usages=False,
)

```

#### ⚙️ Parameters

**include_usages:** `typing.Optional[bool]` — Whether to include active usages of the webhook, only usable by admins


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## SpeechToText
client.speech_to_text.convert(...)

#### 📝 Description

Transcribe an audio or video file. If webhook is set to true, the request will be processed asynchronously and results sent to configured webhooks. When use_multi_channel is true and the provided audio has multiple channels, a 'transcripts' object with separate transcripts for each channel is returned. Otherwise, returns a single transcript. The optional webhook_metadata parameter allows you to attach custom data that will be included in webhook responses for request correlation and tracking.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.speech_to_text.convert(
    enable_logging=True,
    model_id="model_id",
)

```

#### ⚙️ Parameters

**model_id:** `str` — The ID of the model to use for transcription, currently only 'scribe_v1' and 'scribe_v1_experimental' are available.


**enable_logging:** `typing.Optional[bool]` — When enable_logging is set to false zero retention mode will be used for the request. This will mean log and transcript storage features are unavailable for this request. Zero retention mode may only be used by enterprise customers.


**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**language_code:** `typing.Optional[str]` — An ISO-639-1 or ISO-639-3 language_code corresponding to the language of the audio file. Can sometimes improve transcription performance if known beforehand. Defaults to null, in this case the language is predicted automatically.


**tag_audio_events:** `typing.Optional[bool]` — Whether to tag audio events like (laughter), (footsteps), etc. in the transcription.


**num_speakers:** `typing.Optional[int]` — The maximum amount of speakers talking in the uploaded file. Can help with predicting who speaks when. The maximum amount of speakers that can be predicted is 32. Defaults to null, in this case the amount of speakers is set to the maximum value the model supports.


**timestamps_granularity:** `typing.Optional[SpeechToTextConvertRequestTimestampsGranularity]` — The granularity of the timestamps in the transcription. 'word' provides word-level timestamps and 'character' provides character-level timestamps per word.


**diarize:** `typing.Optional[bool]` — Whether to annotate which speaker is currently talking in the uploaded file.


**diarization_threshold:** `typing.Optional[float]` — Diarization threshold to apply during speaker diarization. A higher value means there will be a lower chance of one speaker being diarized as two different speakers but also a higher chance of two different speakers being diarized as one speaker (less total speakers predicted). A low value means there will be a higher chance of one speaker being diarized as two different speakers but also a lower chance of two different speakers being diarized as one speaker (more total speakers predicted). Can only be set when diarize=True and num_speakers=None. Defaults to None, in which case we will choose a threshold based on the model_id (0.22 usually).


**additional_formats:** `typing.Optional[AdditionalFormats]` — A list of additional formats to export the transcript to.


**file_format:** `typing.Optional[SpeechToTextConvertRequestFileFormat]` — The format of input audio. Options are 'pcm_s16le_16' or 'other' For `pcm_s16le_16`, the input audio must be 16-bit PCM at a 16kHz sample rate, single channel (mono), and little-endian byte order. Latency will be lower than with passing an encoded waveform.


**cloud_storage_url:** `typing.Optional[str]` — The HTTPS URL of the file to transcribe. Exactly one of the file or cloud_storage_url parameters must be provided. The file must be accessible via HTTPS and the file size must be less than 2GB. Any valid HTTPS URL is accepted, including URLs from cloud storage providers (AWS S3, Google Cloud Storage, Cloudflare R2, etc.), CDNs, or any other HTTPS source. URLs can be pre-signed or include authentication tokens in query parameters.


**webhook:** `typing.Optional[bool]` — Whether to send the transcription result to configured speech-to-text webhooks.  If set the request will return early without the transcription, which will be delivered later via webhook.


**webhook_id:** `typing.Optional[str]` — Optional specific webhook ID to send the transcription result to. Only valid when webhook is set to true. If not provided, transcription will be sent to all configured speech-to-text webhooks.


**temperature:** `typing.Optional[float]` — Controls the randomness of the transcription output. Accepts values between 0.0 and 2.0, where higher values result in more diverse and less deterministic results. If omitted, we will use a temperature based on the model you selected which is usually 0.


**seed:** `typing.Optional[int]` — If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be an integer between 0 and 2147483647.


**use_multi_channel:** `typing.Optional[bool]` — Whether the audio file contains multiple channels where each channel contains a single speaker. When enabled, each channel will be transcribed independently and the results will be combined. Each word in the response will include a 'channel_index' field indicating which channel it was spoken on. A maximum of 5 channels is supported.


**webhook_metadata:** `typing.Optional[SpeechToTextConvertRequestWebhookMetadata]` — Optional metadata to be included in the webhook response. This should be a JSON string representing an object with a maximum depth of 2 levels and maximum size of 16KB. Useful for tracking internal IDs, job references, or other contextual information.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ForcedAlignment
client.forced_alignment.create(...)

#### 📝 Description

Force align an audio file to text. Use this endpoint to get the timing information for each character and word in an audio file based on a provided text transcript.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.forced_alignment.create(
    text="text",
)

```

#### ⚙️ Parameters

**file:** `from __future__ import annotations

core.File` — See core.File for more documentation


**text:** `str` — The text to align with the audio. The input text can be in any format, however diarization is not supported at this time.


**enabled_spooled_file:** `typing.Optional[bool]` — If true, the file will be streamed to the server and processed in chunks. This is useful for large files that cannot be loaded into memory. The default is false.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi
client.conversational_ai.add_to_knowledge_base(...)

#### 📝 Description

Upload a file or webpage URL to create a knowledge base document.   After creating the document, update the agent's knowledge base by calling [Update agent](/docs/api-reference/agents/update).

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.add_to_knowledge_base(
    agent_id="agent_id",
)

```

#### ⚙️ Parameters

**agent_id:** `typing.Optional[str]`


**name:** `typing.Optional[str]` — A custom, human-readable name for the document.


**url:** `typing.Optional[str]` — URL to a page of documentation that the agent will have access to in order to interact with users.


**file:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.get_document_rag_indexes(...)

#### 📝 Description

Provides information about all RAG indexes of the specified knowledgebase document.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.get_document_rag_indexes(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.delete_document_rag_index(...)

#### 📝 Description

Delete RAG index for the knowledgebase document.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.delete_document_rag_index(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    rag_index_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**rag_index_id:** `str` — The id of RAG index of document from the knowledge base.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.rag_index_overview()

#### 📝 Description

Provides total size and other information of RAG indexes used by knowledgebase documents

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.rag_index_overview()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Music
client.music.compose(...)

#### 📝 Description

Compose a song from a prompt or a composition plan.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.music.compose()

```

#### ⚙️ Parameters

**output_format:** `typing.Optional[MusicComposeRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**prompt:** `typing.Optional[str]` — A simple text prompt to generate a song from. Cannot be used in conjunction with `composition_plan`.


**composition_plan:** `typing.Optional[MusicPrompt]` — A detailed composition plan to guide music generation. Cannot be used in conjunction with `prompt`.


**music_length_ms:** `typing.Optional[int]` — The length of the song to generate in milliseconds. Used only in conjunction with `prompt`. Must be between 3000ms and 300000ms. Optional - if not provided, the model will choose a length based on the prompt.


**model_id:** `typing.Optional[typing.Literal["music_v1"]]` — The model to use for the generation.


**force_instrumental:** `typing.Optional[bool]` — If true, guarantees that the generated song will be instrumental. If false, the song may or may not be instrumental depending on the `prompt`. Can only be used with `prompt`.


**respect_sections_durations:** `typing.Optional[bool]` — Controls how strictly section durations in the `composition_plan` are enforced. Only used with `composition_plan`. When set to true, the model will precisely respect each section's `duration_ms` from the plan. When set to false, the model may adjust individual section durations which will generally lead to better generation quality and improved latency, while always preserving the total song duration from the plan.


**store_for_inpainting:** `typing.Optional[bool]` — Whether to store the generated song for inpainting. Only available to enterprise clients with access to the inpainting API.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.music.compose_detailed(...)

#### 📝 Description

Compose a song from a prompt or a composition plan.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.music.compose_detailed()

```

#### ⚙️ Parameters

**output_format:** `typing.Optional[MusicComposeDetailedRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**prompt:** `typing.Optional[str]` — A simple text prompt to generate a song from. Cannot be used in conjunction with `composition_plan`.


**composition_plan:** `typing.Optional[MusicPrompt]` — A detailed composition plan to guide music generation. Cannot be used in conjunction with `prompt`.


**music_length_ms:** `typing.Optional[int]` — The length of the song to generate in milliseconds. Used only in conjunction with `prompt`. Must be between 3000ms and 300000ms. Optional - if not provided, the model will choose a length based on the prompt.


**model_id:** `typing.Optional[typing.Literal["music_v1"]]` — The model to use for the generation.


**force_instrumental:** `typing.Optional[bool]` — If true, guarantees that the generated song will be instrumental. If false, the song may or may not be instrumental depending on the `prompt`. Can only be used with `prompt`.


**store_for_inpainting:** `typing.Optional[bool]` — Whether to store the generated song for inpainting. Only available to enterprise clients with access to the inpainting API.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.music.stream(...)

#### 📝 Description

Stream a composed song from a prompt or a composition plan.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.music.stream()

```

#### ⚙️ Parameters

**output_format:** `typing.Optional[MusicStreamRequestOutputFormat]` — Output format of the generated audio. Formatted as codec_sample_rate_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3_22050_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.


**prompt:** `typing.Optional[str]` — A simple text prompt to generate a song from. Cannot be used in conjunction with `composition_plan`.


**composition_plan:** `typing.Optional[MusicPrompt]` — A detailed composition plan to guide music generation. Cannot be used in conjunction with `prompt`.


**music_length_ms:** `typing.Optional[int]` — The length of the song to generate in milliseconds. Used only in conjunction with `prompt`. Must be between 3000ms and 300000ms. Optional - if not provided, the model will choose a length based on the prompt.


**model_id:** `typing.Optional[typing.Literal["music_v1"]]` — The model to use for the generation.


**force_instrumental:** `typing.Optional[bool]` — If true, guarantees that the generated song will be instrumental. If false, the song may or may not be instrumental depending on the `prompt`. Can only be used with `prompt`.


**store_for_inpainting:** `typing.Optional[bool]` — Whether to store the generated song for inpainting. Only available to enterprise clients with access to the inpainting API.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## ConversationalAi Conversations
client.conversational_ai.conversations.get_signed_url(...)

#### 📝 Description

Get a signed url to start a conversation with an agent with an agent that requires authorization

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.conversations.get_signed_url(
    agent_id="21m00Tcm4TlvDq8ikWAM",
    include_conversation_id=True,
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of the agent you're taking the action on.


**include_conversation_id:** `typing.Optional[bool]` — Whether to include a conversation_id with the response. If included, the conversation_signature cannot be used again.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.conversations.get_webrtc_token(...)

#### 📝 Description

Get a WebRTC session token for real-time communication.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.conversations.get_webrtc_token(
    agent_id="21m00Tcm4TlvDq8ikWAM",
    participant_name="participant_name",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of the agent you're taking the action on.


**participant_name:** `typing.Optional[str]` — Optional custom participant name. If not provided, user ID will be used


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.conversations.list(...)

#### 📝 Description

Get all conversations of agents that user owns. With option to restrict to a specific agent.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.conversations.list(
    cursor="cursor",
    agent_id="agent_id",
    call_successful="success",
    call_start_before_unix=1,
    call_start_after_unix=1,
    call_duration_min_secs=1,
    call_duration_max_secs=1,
    user_id="user_id",
    page_size=1,
    summary_mode="exclude",
    search="search",
)

```

#### ⚙️ Parameters

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**agent_id:** `typing.Optional[str]` — The id of the agent you're taking the action on.


**call_successful:** `typing.Optional[EvaluationSuccessResult]` — The result of the success evaluation


**call_start_before_unix:** `typing.Optional[int]` — Unix timestamp (in seconds) to filter conversations up to this start date.


**call_start_after_unix:** `typing.Optional[int]` — Unix timestamp (in seconds) to filter conversations after to this start date.


**call_duration_min_secs:** `typing.Optional[int]` — Minimum call duration in seconds.


**call_duration_max_secs:** `typing.Optional[int]` — Maximum call duration in seconds.


**user_id:** `typing.Optional[str]` — Filter conversations by the user ID who initiated them.


**evaluation_params:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Evaluation filters. Repeat param. Format: criteria_id:result. Example: eval=value_framing:success


**data_collection_params:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Data collection filters. Repeat param. Format: id:op:value where op is one of eq|neq|gt|gte|lt|lte|in|exists|missing. For in, pipe-delimit values.


**tool_names:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter conversations by tool names used during the call.


**page_size:** `typing.Optional[int]` — How many conversations to return at maximum. Can not exceed 100, defaults to 30.


**summary_mode:** `typing.Optional[ConversationsListRequestSummaryMode]` — Whether to include transcript summaries in the response.


**search:** `typing.Optional[str]` — Full-text or fuzzy search over transcript messages


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.conversations.get(...)

#### 📝 Description

Get the details of a particular conversation

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.conversations.get(
    conversation_id="123",
)

```

#### ⚙️ Parameters

**conversation_id:** `str` — The id of the conversation you're taking the action on.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.conversations.delete(...)

#### 📝 Description

Delete a particular conversation

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.conversations.delete(
    conversation_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**conversation_id:** `str` — The id of the conversation you're taking the action on.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Twilio
client.conversational_ai.twilio.outbound_call(...)

#### 📝 Description

Handle an outbound call via Twilio

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.twilio.outbound_call(
    agent_id="agent_id",
    agent_phone_number_id="agent_phone_number_id",
    to_number="to_number",
)

```

#### ⚙️ Parameters

**agent_id:** `str`


**agent_phone_number_id:** `str`


**to_number:** `str`


**conversation_initiation_client_data:** `typing.Optional[ConversationInitiationClientDataRequestInput]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Agents
client.conversational_ai.agents.create(...)

#### 📝 Description

Create an agent from a config object

#### 🔌 Usage

```python
from elevenlabs import ConversationalConfig, ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.create(
    conversation_config=ConversationalConfig(),
)

```

#### ⚙️ Parameters

**conversation_config:** `ConversationalConfig` — Conversation configuration for an agent


**platform_settings:** `typing.Optional[AgentPlatformSettingsRequestModel]` — Platform settings for the agent are all settings that aren't related to the conversation orchestration and content.


**workflow:** `typing.Optional[AgentWorkflowRequestModel]` — Workflow for the agent. This is used to define the flow of the conversation and how the agent interacts with tools.


**name:** `typing.Optional[str]` — A name to make the agent easier to find


**tags:** `typing.Optional[typing.Sequence[str]]` — Tags to help classify and filter the agent


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.agents.get(...)

#### 📝 Description

Retrieve config for an agent

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.get(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.agents.delete(...)

#### 📝 Description

Delete an agent

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.delete(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.agents.update(...)

#### 📝 Description

Patches an Agent settings

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.update(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**conversation_config:** `typing.Optional[ConversationalConfig]` — Conversation configuration for an agent


**platform_settings:** `typing.Optional[AgentPlatformSettingsRequestModel]` — Platform settings for the agent are all settings that aren't related to the conversation orchestration and content.


**workflow:** `typing.Optional[AgentWorkflowRequestModel]` — Workflow for the agent. This is used to define the flow of the conversation and how the agent interacts with tools.


**name:** `typing.Optional[str]` — A name to make the agent easier to find


**tags:** `typing.Optional[typing.Sequence[str]]` — Tags to help classify and filter the agent


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.agents.list(...)

#### 📝 Description

Returns a list of your agents and their metadata.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.list(
    page_size=1,
    search="search",
    archived=True,
    sort_direction="asc",
    sort_by="name",
    cursor="cursor",
)

```

#### ⚙️ Parameters

**page_size:** `typing.Optional[int]` — How many Agents to return at maximum. Can not exceed 100, defaults to 30.


**search:** `typing.Optional[str]` — Search by agents name.


**archived:** `typing.Optional[bool]` — Filter agents by archived status


**sort_direction:** `typing.Optional[SortDirection]` — The direction to sort the results


**sort_by:** `typing.Optional[AgentSortBy]` — The field to sort the results by


**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.agents.duplicate(...)

#### 📝 Description

Create a new agent by duplicating an existing one

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.duplicate(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**name:** `typing.Optional[str]` — A name to make the agent easier to find


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.agents.simulate_conversation(...)

#### 📝 Description

Run a conversation between the agent and a simulated user.

#### 🔌 Usage

```python
from elevenlabs import (
    AgentConfig,
    ConversationSimulationSpecification,
    ElevenLabs,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.simulate_conversation(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
    simulation_specification=ConversationSimulationSpecification(
        simulated_user_config=AgentConfig(
            first_message="Hello, how can I help you today?",
            language="en",
            disable_first_message_interruptions=False,
        ),
    ),
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**simulation_specification:** `ConversationSimulationSpecification` — A specification detailing how the conversation should be simulated


**extra_evaluation_criteria:** `typing.Optional[typing.Sequence[PromptEvaluationCriteria]]` — A list of evaluation criteria to test


**new_turns_limit:** `typing.Optional[int]` — Maximum number of new turns to generate in the conversation simulation


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.agents.simulate_conversation_stream(...)

#### 📝 Description

Run a conversation between the agent and a simulated user and stream back the response. Response is streamed back as partial lists of messages that should be concatenated and once the conversation has complete a single final message with the conversation analysis will be sent.

#### 🔌 Usage

```python
from elevenlabs import (
    AgentConfig,
    ConversationSimulationSpecification,
    ElevenLabs,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.simulate_conversation_stream(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
    simulation_specification=ConversationSimulationSpecification(
        simulated_user_config=AgentConfig(
            first_message="Hello, how can I help you today?",
            language="en",
            disable_first_message_interruptions=False,
        ),
    ),
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**simulation_specification:** `ConversationSimulationSpecification` — A specification detailing how the conversation should be simulated


**extra_evaluation_criteria:** `typing.Optional[typing.Sequence[PromptEvaluationCriteria]]` — A list of evaluation criteria to test


**new_turns_limit:** `typing.Optional[int]` — Maximum number of new turns to generate in the conversation simulation


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.agents.run_tests(...)

#### 📝 Description

Run selected tests on the agent with provided configuration. If the agent configuration is provided, it will be used to override default agent configuration.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs, SingleTestRunRequestModel

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.run_tests(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
    tests=[
        SingleTestRunRequestModel(
            test_id="test_id",
        )
    ],
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**tests:** `typing.Sequence[SingleTestRunRequestModel]` — List of tests to run on the agent


**agent_config_override:** `typing.Optional[AdhocAgentConfigOverrideForTestRequestModel]` — Configuration overrides to use for testing. If not provided, the agent's default configuration will be used.


**branch_id:** `typing.Optional[str]` — ID of the branch to run the tests on. If not provided, the tests will be run on the agent default configuration.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Tests
client.conversational_ai.tests.create(...)

#### 📝 Description

Creates a new agent response test.

#### 🔌 Usage

```python
from elevenlabs import (
    AgentFailureResponseExample,
    AgentSuccessfulResponseExample,
    ConversationHistoryTranscriptCommonModelInput,
    ElevenLabs,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.create(
    chat_history=[
        ConversationHistoryTranscriptCommonModelInput(
            role="user",
            time_in_call_secs=1,
        )
    ],
    success_condition="success_condition",
    success_examples=[
        AgentSuccessfulResponseExample(
            response="response",
        )
    ],
    failure_examples=[
        AgentFailureResponseExample(
            response="response",
        )
    ],
    name="name",
)

```

#### ⚙️ Parameters

**chat_history:** `typing.Sequence[ConversationHistoryTranscriptCommonModelInput]`


**success_condition:** `str` — A prompt that evaluates whether the agent's response is successful. Should return True or False.


**success_examples:** `typing.Sequence[AgentSuccessfulResponseExample]` — Non-empty list of example responses that should be considered successful


**failure_examples:** `typing.Sequence[AgentFailureResponseExample]` — Non-empty list of example responses that should be considered failures


**name:** `str`


**tool_call_parameters:** `typing.Optional[UnitTestToolCallEvaluationModelInput]` — How to evaluate the agent's tool call (if any). If empty, the tool call is not evaluated.


**dynamic_variables:** `typing.Optional[
    typing.Dict[
        str, typing.Optional[CreateUnitTestRequestDynamicVariablesValue]
    ]
]` — Dynamic variables to replace in the agent config during testing


**type:** `typing.Optional[UnitTestCommonModelType]`


**from_conversation_metadata:** `typing.Optional[TestFromConversationMetadataInput]` — Metadata of a conversation this test was created from (if applicable).


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tests.get(...)

#### 📝 Description

Gets an agent response test by ID.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.get(
    test_id="TeaqRRdTcIfIu2i7BYfT",
)

```

#### ⚙️ Parameters

**test_id:** `str` — The id of a chat response test. This is returned on test creation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tests.update(...)

#### 📝 Description

Updates an agent response test by ID.

#### 🔌 Usage

```python
from elevenlabs import (
    AgentFailureResponseExample,
    AgentSuccessfulResponseExample,
    ConversationHistoryTranscriptCommonModelInput,
    ElevenLabs,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.update(
    test_id="TeaqRRdTcIfIu2i7BYfT",
    chat_history=[
        ConversationHistoryTranscriptCommonModelInput(
            role="user",
            time_in_call_secs=1,
        )
    ],
    success_condition="success_condition",
    success_examples=[
        AgentSuccessfulResponseExample(
            response="response",
        )
    ],
    failure_examples=[
        AgentFailureResponseExample(
            response="response",
        )
    ],
    name="name",
)

```

#### ⚙️ Parameters

**test_id:** `str` — The id of a chat response test. This is returned on test creation.


**chat_history:** `typing.Sequence[ConversationHistoryTranscriptCommonModelInput]`


**success_condition:** `str` — A prompt that evaluates whether the agent's response is successful. Should return True or False.


**success_examples:** `typing.Sequence[AgentSuccessfulResponseExample]` — Non-empty list of example responses that should be considered successful


**failure_examples:** `typing.Sequence[AgentFailureResponseExample]` — Non-empty list of example responses that should be considered failures


**name:** `str`


**tool_call_parameters:** `typing.Optional[UnitTestToolCallEvaluationModelInput]` — How to evaluate the agent's tool call (if any). If empty, the tool call is not evaluated.


**dynamic_variables:** `typing.Optional[
    typing.Dict[
        str, typing.Optional[UpdateUnitTestRequestDynamicVariablesValue]
    ]
]` — Dynamic variables to replace in the agent config during testing


**type:** `typing.Optional[UnitTestCommonModelType]`


**from_conversation_metadata:** `typing.Optional[TestFromConversationMetadataInput]` — Metadata of a conversation this test was created from (if applicable).


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tests.delete(...)

#### 📝 Description

Deletes an agent response test by ID.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.delete(
    test_id="TeaqRRdTcIfIu2i7BYfT",
)

```

#### ⚙️ Parameters

**test_id:** `str` — The id of a chat response test. This is returned on test creation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tests.summaries(...)

#### 📝 Description

Gets multiple agent response tests by their IDs. Returns a dictionary mapping test IDs to test summaries.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.summaries(
    test_ids=["test_id_1", "test_id_2"],
)

```

#### ⚙️ Parameters

**test_ids:** `typing.Sequence[str]` — List of test IDs to fetch. No duplicates allowed.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tests.list(...)

#### 📝 Description

Lists all agent response tests with pagination support and optional search filtering.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.list(
    cursor="cursor",
    page_size=1,
    search="search",
)

```

#### ⚙️ Parameters

**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**page_size:** `typing.Optional[int]` — How many Tests to return at maximum. Can not exceed 100, defaults to 30.


**search:** `typing.Optional[str]` — Search query to filter tests by name.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi PhoneNumbers
client.conversational_ai.phone_numbers.list()

#### 📝 Description

Retrieve all Phone Numbers

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.phone_numbers.list()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.phone_numbers.create(...)

#### 📝 Description

Import Phone Number from provider configuration (Twilio or SIP trunk)

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.phone_numbers import (
    PhoneNumbersCreateRequestBody_Twilio,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.phone_numbers.create(
    request=PhoneNumbersCreateRequestBody_Twilio(
        phone_number="phone_number",
        label="label",
        sid="sid",
        token="token",
    ),
)

```

#### ⚙️ Parameters

**request:** `PhoneNumbersCreateRequestBody`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.phone_numbers.get(...)

#### 📝 Description

Retrieve Phone Number details by ID

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.phone_numbers.get(
    phone_number_id="TeaqRRdTcIfIu2i7BYfT",
)

```

#### ⚙️ Parameters

**phone_number_id:** `str` — The id of an agent. This is returned on agent creation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.phone_numbers.delete(...)

#### 📝 Description

Delete Phone Number by ID

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.phone_numbers.delete(
    phone_number_id="TeaqRRdTcIfIu2i7BYfT",
)

```

#### ⚙️ Parameters

**phone_number_id:** `str` — The id of an agent. This is returned on agent creation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.phone_numbers.update(...)

#### 📝 Description

Update assigned agent of a phone number

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.phone_numbers.update(
    phone_number_id="TeaqRRdTcIfIu2i7BYfT",
)

```

#### ⚙️ Parameters

**phone_number_id:** `str` — The id of an agent. This is returned on agent creation.


**agent_id:** `typing.Optional[str]`


**inbound_trunk_config:** `typing.Optional[InboundSipTrunkConfigRequestModel]`


**outbound_trunk_config:** `typing.Optional[OutboundSipTrunkConfigRequestModel]`


**livekit_stack:** `typing.Optional[LivekitStackType]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi LlmUsage
client.conversational_ai.llm_usage.calculate(...)

#### 📝 Description

Returns a list of LLM models and the expected cost for using them based on the provided values.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.llm_usage.calculate(
    prompt_length=1,
    number_of_pages=1,
    rag_enabled=True,
)

```

#### ⚙️ Parameters

**prompt_length:** `int` — Length of the prompt in characters.


**number_of_pages:** `int` — Pages of content in PDF documents or URLs in the agent's knowledge base.


**rag_enabled:** `bool` — Whether RAG is enabled.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi KnowledgeBase
client.conversational_ai.knowledge_base.list(...)

#### 📝 Description

Get a list of available knowledge base documents

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.list(
    page_size=1,
    search="search",
    show_only_owned_documents=True,
    sort_direction="asc",
    sort_by="name",
    use_typesense=True,
    cursor="cursor",
)

```

#### ⚙️ Parameters

**page_size:** `typing.Optional[int]` — How many documents to return at maximum. Can not exceed 100, defaults to 30.


**search:** `typing.Optional[str]` — If specified, the endpoint returns only such knowledge base documents whose names start with this string.


**show_only_owned_documents:** `typing.Optional[bool]` — If set to true, the endpoint will return only documents owned by you (and not shared from somebody else).


**types:** `typing.Optional[
    typing.Union[
        KnowledgeBaseDocumentType, typing.Sequence[KnowledgeBaseDocumentType]
    ]
]` — If present, the endpoint will return only documents of the given types.


**sort_direction:** `typing.Optional[SortDirection]` — The direction to sort the results


**sort_by:** `typing.Optional[KnowledgeBaseSortBy]` — The field to sort the results by


**use_typesense:** `typing.Optional[bool]` — If set to true, the endpoint will use typesense DB to search for the documents).


**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Tools
client.conversational_ai.tools.list()

#### 📝 Description

Get all available tools in the workspace.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tools.list()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tools.create(...)

#### 📝 Description

Add a new tool to the available tools in the workspace.

#### 🔌 Usage

```python
from elevenlabs import (
    ElevenLabs,
    LiteralJsonSchemaProperty,
    ObjectJsonSchemaPropertyInput,
    QueryParamsJsonSchema,
    ToolRequestModel,
    ToolRequestModelToolConfig_ApiIntegrationWebhook,
    WebhookToolApiSchemaConfigInput,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tools.create(
    request=ToolRequestModel(
        tool_config=ToolRequestModelToolConfig_ApiIntegrationWebhook(
            name="name",
            description="description",
            api_integration_id="api_integration_id",
            api_integration_connection_id="api_integration_connection_id",
            base_api_schema=WebhookToolApiSchemaConfigInput(
                url="https://example.com/agents/{agent_id}",
                method="GET",
                path_params_schema={
                    "agent_id": LiteralJsonSchemaProperty(
                        type="string",
                    )
                },
                query_params_schema=QueryParamsJsonSchema(
                    properties={
                        "key": LiteralJsonSchemaProperty(
                            type="string",
                            description="My property",
                            is_system_provided=False,
                            dynamic_variable="",
                            constant_value="",
                        )
                    },
                ),
                request_body_schema=ObjectJsonSchemaPropertyInput(),
                request_headers={"Authorization": "Bearer {api_key}"},
            ),
        ),
    ),
)

```

#### ⚙️ Parameters

**request:** `ToolRequestModel`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tools.get(...)

#### 📝 Description

Get tool that is available in the workspace.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tools.get(
    tool_id="tool_id",
)

```

#### ⚙️ Parameters

**tool_id:** `str` — ID of the requested tool.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tools.delete(...)

#### 📝 Description

Delete tool from the workspace.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tools.delete(
    tool_id="tool_id",
)

```

#### ⚙️ Parameters

**tool_id:** `str` — ID of the requested tool.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tools.update(...)

#### 📝 Description

Update tool that is available in the workspace.

#### 🔌 Usage

```python
from elevenlabs import (
    ElevenLabs,
    LiteralJsonSchemaProperty,
    ObjectJsonSchemaPropertyInput,
    QueryParamsJsonSchema,
    ToolRequestModel,
    ToolRequestModelToolConfig_ApiIntegrationWebhook,
    WebhookToolApiSchemaConfigInput,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tools.update(
    tool_id="tool_id",
    request=ToolRequestModel(
        tool_config=ToolRequestModelToolConfig_ApiIntegrationWebhook(
            name="name",
            description="description",
            api_integration_id="api_integration_id",
            api_integration_connection_id="api_integration_connection_id",
            base_api_schema=WebhookToolApiSchemaConfigInput(
                url="https://example.com/agents/{agent_id}",
                method="GET",
                path_params_schema={
                    "agent_id": LiteralJsonSchemaProperty(
                        type="string",
                    )
                },
                query_params_schema=QueryParamsJsonSchema(
                    properties={
                        "key": LiteralJsonSchemaProperty(
                            type="string",
                            description="My property",
                            is_system_provided=False,
                            dynamic_variable="",
                            constant_value="",
                        )
                    },
                ),
                request_body_schema=ObjectJsonSchemaPropertyInput(),
                request_headers={"Authorization": "Bearer {api_key}"},
            ),
        ),
    ),
)

```

#### ⚙️ Parameters

**tool_id:** `str` — ID of the requested tool.


**request:** `ToolRequestModel`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tools.get_dependent_agents(...)

#### 📝 Description

Get a list of agents depending on this tool

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tools.get_dependent_agents(
    tool_id="tool_id",
    cursor="cursor",
    page_size=1,
)

```

#### ⚙️ Parameters

**tool_id:** `str` — ID of the requested tool.


**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**page_size:** `typing.Optional[int]` — How many documents to return at maximum. Can not exceed 100, defaults to 30.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Settings
client.conversational_ai.settings.get()

#### 📝 Description

Retrieve Convai settings for the workspace

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.settings.get()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.settings.update(...)

#### 📝 Description

Update Convai settings for the workspace

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.settings.update()

```

#### ⚙️ Parameters

**conversation_initiation_client_data_webhook:** `typing.Optional[ConversationInitiationClientDataWebhook]`


**webhooks:** `typing.Optional[ConvAiWebhooks]`


**can_use_mcp_servers:** `typing.Optional[bool]` — Whether the workspace can use MCP servers


**rag_retention_period_days:** `typing.Optional[int]`


**default_livekit_stack:** `typing.Optional[LivekitStackType]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Secrets
client.conversational_ai.secrets.list()

#### 📝 Description

Get all workspace secrets for the user

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.secrets.list()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.secrets.create(...)

#### 📝 Description

Create a new secret for the workspace

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.secrets.create(
    name="name",
    value="value",
)

```

#### ⚙️ Parameters

**name:** `str`


**value:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.secrets.delete(...)

#### 📝 Description

Delete a workspace secret if it's not in use

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.secrets.delete(
    secret_id="secret_id",
)

```

#### ⚙️ Parameters

**secret_id:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.secrets.update(...)

#### 📝 Description

Update an existing secret for the workspace

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.secrets.update(
    secret_id="secret_id",
    name="name",
    value="value",
)

```

#### ⚙️ Parameters

**secret_id:** `str`


**name:** `str`


**value:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi BatchCalls
client.conversational_ai.batch_calls.create(...)

#### 📝 Description

Submit a batch call request to schedule calls for multiple recipients.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs, OutboundCallRecipient

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.batch_calls.create(
    call_name="call_name",
    agent_id="agent_id",
    recipients=[OutboundCallRecipient()],
)

```

#### ⚙️ Parameters

**call_name:** `str`


**agent_id:** `str`


**recipients:** `typing.Sequence[OutboundCallRecipient]`


**scheduled_time_unix:** `typing.Optional[int]`


**agent_phone_number_id:** `typing.Optional[str]`


**agent_whatsapp_business_account_id:** `typing.Optional[str]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.batch_calls.list(...)

#### 📝 Description

Get all batch calls for the current workspace.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.batch_calls.list(
    limit=1,
    last_doc="last_doc",
)

```

#### ⚙️ Parameters

**limit:** `typing.Optional[int]`


**last_doc:** `typing.Optional[str]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.batch_calls.get(...)

#### 📝 Description

Get detailed information about a batch call including all recipients.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.batch_calls.get(
    batch_id="batch_id",
)

```

#### ⚙️ Parameters

**batch_id:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.batch_calls.cancel(...)

#### 📝 Description

Cancel a running batch call and set all recipients to cancelled status.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.batch_calls.cancel(
    batch_id="batch_id",
)

```

#### ⚙️ Parameters

**batch_id:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.batch_calls.retry(...)

#### 📝 Description

Retry a batch call, calling failed and no-response recipients again.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.batch_calls.retry(
    batch_id="batch_id",
)

```

#### ⚙️ Parameters

**batch_id:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi SipTrunk
client.conversational_ai.sip_trunk.outbound_call(...)

#### 📝 Description

Handle an outbound call via SIP trunk

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.sip_trunk.outbound_call(
    agent_id="agent_id",
    agent_phone_number_id="agent_phone_number_id",
    to_number="to_number",
)

```

#### ⚙️ Parameters

**agent_id:** `str`


**agent_phone_number_id:** `str`


**to_number:** `str`


**conversation_initiation_client_data:** `typing.Optional[ConversationInitiationClientDataRequestInput]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi McpServers
client.conversational_ai.mcp_servers.list()

#### 📝 Description

Retrieve all MCP server configurations available in the workspace.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.list()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.mcp_servers.create(...)

#### 📝 Description

Create a new MCP server configuration in the workspace.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs, McpServerConfigInput

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.create(
    config=McpServerConfigInput(
        url="url",
        name="name",
    ),
)

```

#### ⚙️ Parameters

**config:** `McpServerConfigInput` — Configuration details for the MCP Server.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.mcp_servers.get(...)

#### 📝 Description

Retrieve a specific MCP server configuration from the workspace.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.get(
    mcp_server_id="mcp_server_id",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.mcp_servers.delete(...)

#### 📝 Description

Delete a specific MCP server configuration from the workspace.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.delete(
    mcp_server_id="mcp_server_id",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.mcp_servers.update(...)

#### 📝 Description

Update the configuration settings for an MCP server.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.update(
    mcp_server_id="mcp_server_id",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**approval_policy:** `typing.Optional[McpApprovalPolicy]` — The approval mode to set for the MCP server


**force_pre_tool_speech:** `typing.Optional[bool]` — If set, overrides the server's force_pre_tool_speech setting for this tool


**disable_interruptions:** `typing.Optional[bool]` — If set, overrides the server's disable_interruptions setting for this tool


**tool_call_sound:** `typing.Optional[ToolCallSoundType]` — Predefined tool call sound type to play during tool execution for all tools from this MCP server


**tool_call_sound_behavior:** `typing.Optional[ToolCallSoundBehavior]` — Determines when the tool call sound should play for all tools from this MCP server


**execution_mode:** `typing.Optional[ToolExecutionMode]` — If set, overrides the server's execution_mode setting for this tool


**request_headers:** `typing.Optional[
    typing.Dict[
        str,
        typing.Optional[McpServerConfigUpdateRequestModelRequestHeadersValue],
    ]
]` — The headers to include in requests to the MCP server


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Agents Widget
client.conversational_ai.agents.widget.get(...)

#### 📝 Description

Retrieve the widget configuration for an agent

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.widget.get(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
    conversation_signature="conversation_signature",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**conversation_signature:** `typing.Optional[str]` — An expiring token that enables a websocket conversation to start. These can be generated for an agent using the /v1/convai/conversation/get-signed-url endpoint


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Agents Link
client.conversational_ai.agents.link.get(...)

#### 📝 Description

Get the current link used to share the agent with others

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.link.get(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Agents KnowledgeBase
client.conversational_ai.agents.knowledge_base.size(...)

#### 📝 Description

Returns the number of pages in the agent's knowledge base.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.knowledge_base.size(
    agent_id="agent_id",
)

```

#### ⚙️ Parameters

**agent_id:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Agents LlmUsage
client.conversational_ai.agents.llm_usage.calculate(...)

#### 📝 Description

Calculates expected number of LLM tokens needed for the specified agent.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.llm_usage.calculate(
    agent_id="agent_id",
)

```

#### ⚙️ Parameters

**agent_id:** `str`


**prompt_length:** `typing.Optional[int]` — Length of the prompt in characters.


**number_of_pages:** `typing.Optional[int]` — Pages of content in pdf documents OR urls in agent's Knowledge Base.


**rag_enabled:** `typing.Optional[bool]` — Whether RAG is enabled.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Agents Widget Avatar
client.conversational_ai.agents.widget.avatar.create(...)

#### 📝 Description

Sets the avatar for an agent displayed in the widget

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.agents.widget.avatar.create(
    agent_id="agent_3701k3ttaq12ewp8b7qv5rfyszkz",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — The id of an agent. This is returned on agent creation.


**avatar_file:** `from __future__ import annotations

core.File` — See core.File for more documentation


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Conversations Audio
client.conversational_ai.conversations.audio.get(...)

#### 📝 Description

Get the audio recording of a particular conversation

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.conversations.audio.get(
    conversation_id="conversation_id",
)

```

#### ⚙️ Parameters

**conversation_id:** `str` — The id of the conversation you're taking the action on.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## ConversationalAi Conversations Feedback
client.conversational_ai.conversations.feedback.create(...)

#### 📝 Description

Send the feedback for the given conversation

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.conversations.feedback.create(
    conversation_id="21m00Tcm4TlvDq8ikWAM",
    feedback="like",
)

```

#### ⚙️ Parameters

**conversation_id:** `str` — The id of the conversation you're taking the action on.


**feedback:** `typing.Optional[UserFeedbackScore]` — Either 'like' or 'dislike' to indicate the feedback for the conversation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Dashboard Settings
client.conversational_ai.dashboard.settings.get()

#### 📝 Description

Retrieve Convai dashboard settings for the workspace

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.dashboard.settings.get()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.dashboard.settings.update(...)

#### 📝 Description

Update Convai dashboard settings for the workspace

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.dashboard.settings.update()

```

#### ⚙️ Parameters

**charts:** `typing.Optional[typing.Sequence[PatchConvAiDashboardSettingsRequestChartsItem]]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi KnowledgeBase Documents
client.conversational_ai.knowledge_base.documents.create_from_url(...)

#### 📝 Description

Create a knowledge base document generated by scraping the given webpage.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.create_from_url(
    url="url",
)

```

#### ⚙️ Parameters

**url:** `str` — URL to a page of documentation that the agent will have access to in order to interact with users.


**name:** `typing.Optional[str]` — A custom, human-readable name for the document.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.knowledge_base.documents.create_from_file(...)

#### 📝 Description

Create a knowledge base document generated form the uploaded file.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.create_from_file()

```

#### ⚙️ Parameters

**file:** `from __future__ import annotations

core.File` — See core.File for more documentation


**name:** `typing.Optional[str]` — A custom, human-readable name for the document.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.knowledge_base.documents.create_from_text(...)

#### 📝 Description

Create a knowledge base document containing the provided text.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.create_from_text(
    text="text",
)

```

#### ⚙️ Parameters

**text:** `str` — Text content to be added to the knowledge base.


**name:** `typing.Optional[str]` — A custom, human-readable name for the document.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.knowledge_base.documents.get(...)

#### 📝 Description

Get details about a specific documentation making up the agent's knowledge base

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.get(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    agent_id="agent_id",
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**agent_id:** `typing.Optional[str]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.knowledge_base.documents.delete(...)

#### 📝 Description

Delete a document from the knowledge base

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.delete(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    force=True,
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**force:** `typing.Optional[bool]` — If set to true, the document will be deleted regardless of whether it is used by any agents and it will be deleted from the dependent agents.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.knowledge_base.documents.update(...)

#### 📝 Description

Update the name of a document

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.update(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    name="name",
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**name:** `str` — A custom, human-readable name for the document.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.knowledge_base.documents.get_agents(...)

#### 📝 Description

Get a list of agents depending on this knowledge base document

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.get_agents(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    cursor="cursor",
    page_size=1,
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**page_size:** `typing.Optional[int]` — How many documents to return at maximum. Can not exceed 100, defaults to 30.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.knowledge_base.documents.get_content(...)

#### 📝 Description

Get the entire content of a document from the knowledge base

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.get_content(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi KnowledgeBase Document
client.conversational_ai.knowledge_base.document.compute_rag_index(...)

#### 📝 Description

In case the document is not RAG indexed, it triggers rag indexing task, otherwise it just returns the current status.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.document.compute_rag_index(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    model="e5_mistral_7b_instruct",
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**model:** `EmbeddingModelEnum`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi KnowledgeBase Documents Chunk
client.conversational_ai.knowledge_base.documents.chunk.get(...)

#### 📝 Description

Get details about a specific documentation part used by RAG.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.knowledge_base.documents.chunk.get(
    documentation_id="21m00Tcm4TlvDq8ikWAM",
    chunk_id="chunk_id",
)

```

#### ⚙️ Parameters

**documentation_id:** `str` — The id of a document from the knowledge base. This is returned on document addition.


**chunk_id:** `str` — The id of a document RAG chunk from the knowledge base.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi McpServers Tools
client.conversational_ai.mcp_servers.tools.list(...)

#### 📝 Description

Retrieve all tools available for a specific MCP server configuration.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.tools.list(
    mcp_server_id="mcp_server_id",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi McpServers ApprovalPolicy
client.conversational_ai.mcp_servers.approval_policy.update(...)

#### 📝 Description

Update the approval policy configuration for an MCP server. DEPRECATED: Use PATCH /mcp-servers/{id} endpoint instead.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.approval_policy.update(
    mcp_server_id="mcp_server_id",
    approval_policy="auto_approve_all",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**approval_policy:** `McpApprovalPolicy` — The approval mode to set for the MCP server


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi McpServers ToolApprovals
client.conversational_ai.mcp_servers.tool_approvals.create(...)

#### 📝 Description

Add approval for a specific MCP tool when using per-tool approval mode.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.tool_approvals.create(
    mcp_server_id="mcp_server_id",
    tool_name="tool_name",
    tool_description="tool_description",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**tool_name:** `str` — The name of the MCP tool


**tool_description:** `str` — The description of the MCP tool


**input_schema:** `typing.Optional[typing.Dict[str, typing.Any]]` — The input schema of the MCP tool (the schema defined on the MCP server before ElevenLabs does any extra processing)


**approval_policy:** `typing.Optional[McpToolApprovalPolicy]` — The tool-level approval policy


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.mcp_servers.tool_approvals.delete(...)

#### 📝 Description

Remove approval for a specific MCP tool when using per-tool approval mode.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.tool_approvals.delete(
    mcp_server_id="mcp_server_id",
    tool_name="tool_name",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**tool_name:** `str` — Name of the MCP tool to remove approval for.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi McpServers ToolConfigs
client.conversational_ai.mcp_servers.tool_configs.create(...)

#### 📝 Description

Create configuration overrides for a specific MCP tool.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.tool_configs.create(
    mcp_server_id="mcp_server_id",
    tool_name="tool_name",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**tool_name:** `str` — The name of the MCP tool


**force_pre_tool_speech:** `typing.Optional[bool]` — If set, overrides the server's force_pre_tool_speech setting for this tool


**disable_interruptions:** `typing.Optional[bool]` — If set, overrides the server's disable_interruptions setting for this tool


**tool_call_sound:** `typing.Optional[ToolCallSoundType]` — If set, overrides the server's tool_call_sound setting for this tool


**tool_call_sound_behavior:** `typing.Optional[ToolCallSoundBehavior]` — If set, overrides the server's tool_call_sound_behavior setting for this tool


**execution_mode:** `typing.Optional[ToolExecutionMode]` — If set, overrides the server's execution_mode setting for this tool


**assignments:** `typing.Optional[typing.Sequence[DynamicVariableAssignment]]` — Dynamic variable assignments for this MCP tool


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.mcp_servers.tool_configs.get(...)

#### 📝 Description

Retrieve configuration overrides for a specific MCP tool.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.tool_configs.get(
    mcp_server_id="mcp_server_id",
    tool_name="tool_name",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**tool_name:** `str` — Name of the MCP tool to retrieve config overrides for.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.mcp_servers.tool_configs.delete(...)

#### 📝 Description

Remove configuration overrides for a specific MCP tool.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.tool_configs.delete(
    mcp_server_id="mcp_server_id",
    tool_name="tool_name",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**tool_name:** `str` — Name of the MCP tool to remove config overrides for.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.mcp_servers.tool_configs.update(...)

#### 📝 Description

Update configuration overrides for a specific MCP tool.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.mcp_servers.tool_configs.update(
    mcp_server_id="mcp_server_id",
    tool_name="tool_name",
)

```

#### ⚙️ Parameters

**mcp_server_id:** `str` — ID of the MCP Server.


**tool_name:** `str` — Name of the MCP tool to update config overrides for.


**force_pre_tool_speech:** `typing.Optional[bool]` — If set, overrides the server's force_pre_tool_speech setting for this tool


**disable_interruptions:** `typing.Optional[bool]` — If set, overrides the server's disable_interruptions setting for this tool


**tool_call_sound:** `typing.Optional[ToolCallSoundType]` — If set, overrides the server's tool_call_sound setting for this tool


**tool_call_sound_behavior:** `typing.Optional[ToolCallSoundBehavior]` — If set, overrides the server's tool_call_sound_behavior setting for this tool


**execution_mode:** `typing.Optional[ToolExecutionMode]` — If set, overrides the server's execution_mode setting for this tool


**assignments:** `typing.Optional[typing.Sequence[DynamicVariableAssignment]]` — Dynamic variable assignments for this MCP tool


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ConversationalAi Tests Invocations
client.conversational_ai.tests.invocations.list(...)

#### 📝 Description

Lists all test invocations with pagination support and optional search filtering.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.invocations.list(
    agent_id="agent_id",
    page_size=1,
    cursor="cursor",
)

```

#### ⚙️ Parameters

**agent_id:** `str` — Filter by agent ID


**page_size:** `typing.Optional[int]` — How many Tests to return at maximum. Can not exceed 100, defaults to 30.


**cursor:** `typing.Optional[str]` — Used for fetching next page. Cursor is returned in the response.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tests.invocations.get(...)

#### 📝 Description

Gets a test invocation by ID.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.invocations.get(
    test_invocation_id="test_invocation_id",
)

```

#### ⚙️ Parameters

**test_invocation_id:** `str` — The id of a test invocation. This is returned when tests are run.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.conversational_ai.tests.invocations.resubmit(...)

#### 📝 Description

Resubmits specific test runs from a test invocation.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.conversational_ai.tests.invocations.resubmit(
    test_invocation_id="test_invocation_id",
    test_run_ids=["test_run_ids"],
    agent_id="agent_id",
)

```

#### ⚙️ Parameters

**test_invocation_id:** `str` — The id of a test invocation. This is returned when tests are run.


**test_run_ids:** `typing.Sequence[str]` — List of test run IDs to resubmit


**agent_id:** `str` — Agent ID to resubmit tests for


**agent_config_override:** `typing.Optional[AdhocAgentConfigOverrideForTestRequestModel]` — Configuration overrides to use for testing. If not provided, the agent's default configuration will be used.


**branch_id:** `typing.Optional[str]` — ID of the branch to run the tests on. If not provided, the tests will be run on the agent default configuration.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Dubbing Resource
client.dubbing.resource.get(...)

#### 📝 Description

Given a dubbing ID generated from the '/v1/dubbing' endpoint with studio enabled, returns the dubbing resource.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.get(
    dubbing_id="dubbing_id",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.resource.transcribe(...)

#### 📝 Description

Regenerate the transcriptions for the specified segments. Does not automatically regenerate translations or dubs.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.transcribe(
    dubbing_id="dubbing_id",
    segments=["segments"],
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**segments:** `typing.Sequence[str]` — Transcribe this specific list of segments.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.resource.translate(...)

#### 📝 Description

Regenerate the translations for either the entire resource or the specified segments/languages. Will automatically transcribe missing transcriptions. Will not automatically regenerate the dubs.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.translate(
    dubbing_id="dubbing_id",
    segments=["segments"],
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**segments:** `typing.Sequence[str]` — Translate only this list of segments.


**languages:** `typing.Optional[typing.Sequence[str]]` — Translate only these languages for each segment.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.resource.dub(...)

#### 📝 Description

Regenerate the dubs for either the entire resource or the specified segments/languages. Will automatically transcribe and translate any missing transcriptions and translations.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.dub(
    dubbing_id="dubbing_id",
    segments=["segments"],
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**segments:** `typing.Sequence[str]` — Dub only this list of segments.


**languages:** `typing.Optional[typing.Sequence[str]]` — Dub only these languages for each segment.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.resource.render(...)

#### 📝 Description

Regenerate the output media for a language using the latest Studio state. Please ensure all segments have been dubbed before rendering, otherwise they will be omitted. Renders are generated asynchronously, and to check the status of all renders please use the 'Get Dubbing Resource' endpoint.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.render(
    dubbing_id="dubbing_id",
    language="language",
    render_type="mp4",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**language:** `str` — Render this language


**render_type:** `RenderType` — The type of the render. One of ['mp4', 'aac', 'mp3', 'wav', 'aaf', 'tracks_zip', 'clips_zip']


**normalize_volume:** `typing.Optional[bool]` — Whether to normalize the volume of the rendered audio.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Dubbing Audio
client.dubbing.audio.get(...)

#### 📝 Description

Returns dub as a streamed MP3 or MP4 file. If this dub has been edited using Dubbing Studio you need to use the resource render endpoint as this endpoint only returns the original automatic dub result.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.audio.get(
    dubbing_id="dubbing_id",
    language_code="language_code",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**language_code:** `str` — ID of the language.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## Dubbing Transcript
client.dubbing.transcript.get_transcript_for_dub(...)

#### 📝 Description

Returns transcript for the dub as an SRT or WEBVTT file.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.transcript.get_transcript_for_dub(
    dubbing_id="dubbing_id",
    language_code="language_code",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**language_code:** `str` — ID of the language.


**format_type:** `typing.Optional[TranscriptGetTranscriptForDubRequestFormatType]` — Format to use for the subtitle file, either 'srt' or 'webvtt'


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Dubbing Resource Language
client.dubbing.resource.language.add(...)

#### 📝 Description

Adds the given ElevenLab Turbo V2/V2.5 language code to the resource. Does not automatically generate transcripts/translations/audio.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.language.add(
    dubbing_id="dubbing_id",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**language:** `typing.Optional[str]` — The Target language.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Dubbing Resource Segment
client.dubbing.resource.segment.update(...)

#### 📝 Description

Modifies a single segment with new text and/or start/end times. Will update the values for only a specific language of a segment. Does not automatically regenerate the dub.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.segment.update(
    dubbing_id="dubbing_id",
    segment_id="segment_id",
    language="language",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**segment_id:** `str` — ID of the segment


**language:** `str` — ID of the language.


**start_time:** `typing.Optional[float]`


**end_time:** `typing.Optional[float]`


**text:** `typing.Optional[str]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.resource.segment.delete(...)

#### 📝 Description

Deletes a single segment from the dubbing.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.segment.delete(
    dubbing_id="dubbing_id",
    segment_id="segment_id",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**segment_id:** `str` — ID of the segment


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Dubbing Resource Speaker
client.dubbing.resource.speaker.update(...)

#### 📝 Description

Amend the metadata associated with a speaker, such as their voice. Both voice cloning and using voices from the ElevenLabs library are supported.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.speaker.update(
    dubbing_id="dubbing_id",
    speaker_id="speaker_id",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**speaker_id:** `str` — ID of the speaker.


**voice_id:** `typing.Optional[str]` — Either the identifier of a voice from the ElevenLabs voice library, or one of ['track-clone', 'clip-clone'].


**languages:** `typing.Optional[typing.Sequence[str]]` — Languages to apply these changes to. If empty, will apply to all languages.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.dubbing.resource.speaker.find_similar_voices(...)

#### 📝 Description

Fetch the top 10 similar voices to a speaker, including the voice IDs, names, descriptions, and, where possible, a sample audio recording.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.speaker.find_similar_voices(
    dubbing_id="dubbing_id",
    speaker_id="speaker_id",
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**speaker_id:** `str` — ID of the speaker.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Dubbing Resource Speaker Segment
client.dubbing.resource.speaker.segment.create(...)

#### 📝 Description

Creates a new segment in dubbing resource with a start and end time for the speaker in every available language. Does not automatically generate transcripts/translations/audio.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.dubbing.resource.speaker.segment.create(
    dubbing_id="dubbing_id",
    speaker_id="speaker_id",
    start_time=1.1,
    end_time=1.1,
)

```

#### ⚙️ Parameters

**dubbing_id:** `str` — ID of the dubbing project.


**speaker_id:** `str` — ID of the speaker.


**start_time:** `float`


**end_time:** `float`


**text:** `typing.Optional[str]`


**translations:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Music CompositionPlan
client.music.composition_plan.create(...)

#### 📝 Description

Create a composition plan for music generation. Usage of this endpoint does not cost any credits but is subject to rate limiting depending on your tier.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.music.composition_plan.create(
    prompt="prompt",
)

```

#### ⚙️ Parameters

**prompt:** `str` — A simple text prompt to compose a plan from.


**music_length_ms:** `typing.Optional[int]` — The length of the composition plan to generate in milliseconds. Must be between 3000ms and 300000ms. Optional - if not provided, the model will choose a length based on the prompt.


**source_composition_plan:** `typing.Optional[MusicPrompt]` — An optional composition plan to use as a source for the new composition plan.


**model_id:** `typing.Optional[typing.Literal["music_v1"]]` — The model to use for the generation.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## PronunciationDictionaries Rules
client.pronunciation_dictionaries.rules.add(...)

#### 📝 Description

Add rules to the pronunciation dictionary

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs
from elevenlabs.pronunciation_dictionaries.rules import (
    PronunciationDictionaryRule_Alias,
)

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.rules.add(
    pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
    rules=[
        PronunciationDictionaryRule_Alias(
            string_to_replace="Thailand",
            alias="tie-land",
        )
    ],
)

```

#### ⚙️ Parameters

**pronunciation_dictionary_id:** `str` — The id of the pronunciation dictionary


**rules:** `typing.Sequence[PronunciationDictionaryRule]`

List of pronunciation rules. Rule can be either:
    an alias rule: {'string_to_replace': 'a', 'type': 'alias', 'alias': 'b', }
    or a phoneme rule: {'string_to_replace': 'a', 'type': 'phoneme', 'phoneme': 'b', 'alphabet': 'ipa' }


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.pronunciation_dictionaries.rules.remove(...)

#### 📝 Description

Remove rules from the pronunciation dictionary

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.pronunciation_dictionaries.rules.remove(
    pronunciation_dictionary_id="21m00Tcm4TlvDq8ikWAM",
    rule_strings=["rule_strings"],
)

```

#### ⚙️ Parameters

**pronunciation_dictionary_id:** `str` — The id of the pronunciation dictionary


**rule_strings:** `typing.Sequence[str]` — List of strings to remove from the pronunciation dictionary.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## ServiceAccounts ApiKeys
client.service_accounts.api_keys.list(...)

#### 📝 Description

Get all API keys for a service account

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.service_accounts.api_keys.list(
    service_account_user_id="service_account_user_id",
)

```

#### ⚙️ Parameters

**service_account_user_id:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.service_accounts.api_keys.create(...)

#### 📝 Description

Create a new API key for a service account

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.service_accounts.api_keys.create(
    service_account_user_id="service_account_user_id",
    name="name",
    permissions=["text_to_speech"],
)

```

#### ⚙️ Parameters

**service_account_user_id:** `str`


**name:** `str`


**permissions:** `BodyCreateServiceAccountApiKeyV1ServiceAccountsServiceAccountUserIdApiKeysPostPermissions` — The permissions of the XI API.


**character_limit:** `typing.Optional[int]` — The character limit of the XI API key. If provided this will limit the usage of this api key to n characters per month where n is the chosen value. Requests that incur charges will fail after reaching this monthly limit.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.service_accounts.api_keys.delete(...)

#### 📝 Description

Delete an existing API key for a service account

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.service_accounts.api_keys.delete(
    service_account_user_id="service_account_user_id",
    api_key_id="api_key_id",
)

```

#### ⚙️ Parameters

**service_account_user_id:** `str`


**api_key_id:** `str`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.service_accounts.api_keys.update(...)

#### 📝 Description

Update an existing API key for a service account

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.service_accounts.api_keys.update(
    service_account_user_id="service_account_user_id",
    api_key_id="api_key_id",
    is_enabled=True,
    name="Sneaky Fox",
    permissions=["text_to_speech"],
)

```

#### ⚙️ Parameters

**service_account_user_id:** `str`


**api_key_id:** `str`


**is_enabled:** `bool` — Whether to enable or disable the API key.


**name:** `str` — The name of the XI API key to use (used for identification purposes only).


**permissions:** `BodyEditServiceAccountApiKeyV1ServiceAccountsServiceAccountUserIdApiKeysApiKeyIdPatchPermissions` — The permissions of the XI API.


**character_limit:** `typing.Optional[int]` — The character limit of the XI API key. If provided this will limit the usage of this api key to n characters per month where n is the chosen value. Requests that incur charges will fail after reaching this monthly limit.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## SpeechToText Transcripts
client.speech_to_text.transcripts.get(...)

#### 📝 Description

Retrieve a previously generated transcript by its ID.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.speech_to_text.transcripts.get(
    transcription_id="transcription_id",
)

```

#### ⚙️ Parameters

**transcription_id:** `str` — The unique ID of the transcript to retrieve


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.speech_to_text.transcripts.delete(...)

#### 📝 Description

Delete a previously generated transcript by its ID.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.speech_to_text.transcripts.delete(
    transcription_id="transcription_id",
)

```

#### ⚙️ Parameters

**transcription_id:** `str` — The unique ID of the transcript to delete


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Studio Projects
client.studio.projects.list()

#### 📝 Description

Returns a list of your Studio projects with metadata.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.list()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.create(...)

#### 📝 Description

Creates a new Studio project, it can be either initialized as blank, from a document or from a URL.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.create(
    name="name",
)

```

#### ⚙️ Parameters

**name:** `str` — The name of the Studio project, used for identification only.


**default_title_voice_id:** `typing.Optional[str]` — The voice_id that corresponds to the default voice used for new titles.


**default_paragraph_voice_id:** `typing.Optional[str]` — The voice_id that corresponds to the default voice used for new paragraphs.


**default_model_id:** `typing.Optional[str]` — The ID of the model to be used for this Studio project, you can query GET /v1/models to list all available models.


**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the Studio project. If this is set, 'from_url' and 'from_content' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.


**from_document:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**from_content_json:** `typing.Optional[str]`

    An optional content to initialize the Studio project with. If this is set, 'from_url' and 'from_document' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.

    Example:
    [{"name": "Chapter A", "blocks": [{"sub_type": "p", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "A", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "B", "type": "tts_node"}]}, {"sub_type": "h1", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "C", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "D", "type": "tts_node"}]}]}, {"name": "Chapter B", "blocks": [{"sub_type": "p", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "E", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "F", "type": "tts_node"}]}, {"sub_type": "h2", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "G", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "H", "type": "tts_node"}]}]}]



**quality_preset:** `typing.Optional[str]`

Output quality of the generated audio. Must be one of:
standard - standard output format, 128kbps with 44.1kHz sample rate.
high - high quality output format, 192kbps with 44.1kHz sample rate and major improvements on our side. Using this setting increases the credit cost by 20%.
ultra - ultra quality output format, 192kbps with 44.1kHz sample rate and highest improvements on our side. Using this setting increases the credit cost by 50%.
ultra lossless - ultra quality output format, 705.6kbps with 44.1kHz sample rate and highest improvements on our side in a fully lossless format. Using this setting increases the credit cost by 100%.


**title:** `typing.Optional[str]` — An optional name of the author of the Studio project, this will be added as metadata to the mp3 file on Studio project or chapter download.


**author:** `typing.Optional[str]` — An optional name of the author of the Studio project, this will be added as metadata to the mp3 file on Studio project or chapter download.


**description:** `typing.Optional[str]` — An optional description of the Studio project.


**genres:** `typing.Optional[typing.List[str]]` — An optional list of genres associated with the Studio project.


**target_audience:** `typing.Optional[ProjectsCreateRequestTargetAudience]` — An optional target audience of the Studio project.


**language:** `typing.Optional[str]` — An optional language of the Studio project. Two-letter language code (ISO 639-1).


**content_type:** `typing.Optional[str]` — An optional content type of the Studio project.


**original_publication_date:** `typing.Optional[str]` — An optional original publication date of the Studio project, in the format YYYY-MM-DD or YYYY.


**mature_content:** `typing.Optional[bool]` — An optional specification of whether this Studio project contains mature content.


**isbn_number:** `typing.Optional[str]` — An optional ISBN number of the Studio project you want to create, this will be added as metadata to the mp3 file on Studio project or chapter download.


**acx_volume_normalization:** `typing.Optional[bool]` — [Deprecated] When the Studio project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements


**volume_normalization:** `typing.Optional[bool]` — When the Studio project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements


**pronunciation_dictionary_locators:** `typing.Optional[typing.List[str]]` — A list of pronunciation dictionary locators (pronunciation_dictionary_id, version_id) encoded as a list of JSON strings for pronunciation dictionaries to be applied to the text. A list of json encoded strings is required as adding projects may occur through formData as opposed to jsonBody. To specify multiple dictionaries use multiple --form lines in your curl, such as --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"Vmd4Zor6fplcA7WrINey\",\"version_id\":\"hRPaxjlTdR7wFMhV4w0b\"}"' --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"JzWtcGQMJ6bnlWwyMo7e\",\"version_id\":\"lbmwxiLu4q6txYxgdZqn\"}"'.


**callback_url:** `typing.Optional[str]`

    A url that will be called by our service when the Studio project is converted. Request will contain a json blob containing the status of the conversion
    Messages:
    1. When project was converted successfully:
    {
      type: "project_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        conversion_status: "success",
        project_snapshot_id: "22m00Tcm4TlvDq8ikMAT",
        error_details: None,
      }
    }
    2. When project conversion failed:
    {
      type: "project_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        conversion_status: "error",
        project_snapshot_id: None,
        error_details: "Error details if conversion failed"
      }
    }

    3. When chapter was converted successfully:
    {
      type: "chapter_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        chapter_id: "22m00Tcm4TlvDq8ikMAT",
        conversion_status: "success",
        chapter_snapshot_id: "23m00Tcm4TlvDq8ikMAV",
        error_details: None,
      }
    }
    4. When chapter conversion failed:
    {
      type: "chapter_conversion_status",
      event_timestamp: 1234567890,
      data: {
        request_id: "1234567890",
        project_id: "21m00Tcm4TlvDq8ikWAM",
        chapter_id: "22m00Tcm4TlvDq8ikMAT",
        conversion_status: "error",
        chapter_snapshot_id: None,
        error_details: "Error details if conversion failed"
      }
    }



**fiction:** `typing.Optional[ProjectsCreateRequestFiction]` — An optional specification of whether the content of this Studio project is fiction.


**apply_text_normalization:** `typing.Optional[ProjectsCreateRequestApplyTextNormalization]`

    This parameter controls text normalization with four modes: 'auto', 'on', 'apply_english' and 'off'.
    When set to 'auto', the system will automatically decide whether to apply text normalization
    (e.g., spelling out numbers). With 'on', text normalization will always be applied, while
    with 'off', it will be skipped. 'apply_english' is the same as 'on' but will assume that text is in English.



**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the Studio project to audio or not.


**auto_assign_voices:** `typing.Optional[bool]` — [Alpha Feature] Whether automatically assign voices to phrases in the create Project.


**source_type:** `typing.Optional[ProjectsCreateRequestSourceType]` — The type of Studio project to create.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.get(...)

#### 📝 Description

Returns information about a specific Studio project. This endpoint returns more detailed information about a project than `GET /v1/studio`.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.get(
    project_id="21m00Tcm4TlvDq8ikWAM",
    share_id="share_id",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**share_id:** `typing.Optional[str]` — The share ID of the project


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.update(...)

#### 📝 Description

Updates the specified Studio project by setting the values of the parameters passed.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.update(
    project_id="21m00Tcm4TlvDq8ikWAM",
    name="Project 1",
    default_title_voice_id="21m00Tcm4TlvDq8ikWAM",
    default_paragraph_voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**name:** `str` — The name of the Studio project, used for identification only.


**default_title_voice_id:** `str` — The voice_id that corresponds to the default voice used for new titles.


**default_paragraph_voice_id:** `str` — The voice_id that corresponds to the default voice used for new paragraphs.


**title:** `typing.Optional[str]` — An optional name of the author of the Studio project, this will be added as metadata to the mp3 file on Studio project or chapter download.


**author:** `typing.Optional[str]` — An optional name of the author of the Studio project, this will be added as metadata to the mp3 file on Studio project or chapter download.


**isbn_number:** `typing.Optional[str]` — An optional ISBN number of the Studio project you want to create, this will be added as metadata to the mp3 file on Studio project or chapter download.


**volume_normalization:** `typing.Optional[bool]` — When the Studio project is downloaded, should the returned audio have postprocessing in order to make it compliant with audiobook normalized volume requirements


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.delete(...)

#### 📝 Description

Deletes a Studio project.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.delete(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.convert(...)

#### 📝 Description

Starts conversion of a Studio project and all of its chapters.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.convert(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Studio Projects PronunciationDictionaries
client.studio.projects.pronunciation_dictionaries.create(...)

#### 📝 Description

Create a set of pronunciation dictionaries acting on a project. This will automatically mark text within this project as requiring reconverting where the new dictionary would apply or the old one no longer does.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs, PronunciationDictionaryVersionLocator

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.pronunciation_dictionaries.create(
    project_id="21m00Tcm4TlvDq8ikWAM",
    pronunciation_dictionary_locators=[
        PronunciationDictionaryVersionLocator(
            pronunciation_dictionary_id="pronunciation_dictionary_id",
        )
    ],
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**pronunciation_dictionary_locators:** `typing.Sequence[PronunciationDictionaryVersionLocator]` — A list of pronunciation dictionary locators (pronunciation_dictionary_id, version_id) encoded as a list of JSON strings for pronunciation dictionaries to be applied to the text. A list of json encoded strings is required as adding projects may occur through formData as opposed to jsonBody. To specify multiple dictionaries use multiple --form lines in your curl, such as --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"Vmd4Zor6fplcA7WrINey\",\"version_id\":\"hRPaxjlTdR7wFMhV4w0b\"}"' --form 'pronunciation_dictionary_locators="{\"pronunciation_dictionary_id\":\"JzWtcGQMJ6bnlWwyMo7e\",\"version_id\":\"lbmwxiLu4q6txYxgdZqn\"}"'.


**invalidate_affected_text:** `typing.Optional[bool]` — This will automatically mark text in this project for reconversion when the new dictionary applies or the old one no longer does.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Studio Projects Content
client.studio.projects.content.update(...)

#### 📝 Description

Updates Studio project content.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.content.update(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the Studio project. If this is set, 'from_url' and 'from_content' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.


**from_document:** `from __future__ import annotations

typing.Optional[core.File]` — See core.File for more documentation


**from_content_json:** `typing.Optional[str]`

    An optional content to initialize the Studio project with. If this is set, 'from_url' and 'from_document' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.

    Example:
    [{"name": "Chapter A", "blocks": [{"sub_type": "p", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "A", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "B", "type": "tts_node"}]}, {"sub_type": "h1", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "C", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "D", "type": "tts_node"}]}]}, {"name": "Chapter B", "blocks": [{"sub_type": "p", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "E", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "F", "type": "tts_node"}]}, {"sub_type": "h2", "nodes": [{"voice_id": "6lCwbsX1yVjD49QmpkT0", "text": "G", "type": "tts_node"}, {"voice_id": "6lCwbsX1yVjD49QmpkT1", "text": "H", "type": "tts_node"}]}]}]



**auto_convert:** `typing.Optional[bool]` — Whether to auto convert the Studio project to audio or not.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Studio Projects Snapshots
client.studio.projects.snapshots.list(...)

#### 📝 Description

Retrieves a list of snapshots for a Studio project.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.snapshots.list(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the Studio project.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.snapshots.get(...)

#### 📝 Description

Returns the project snapshot.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.snapshots.get(
    project_id="21m00Tcm4TlvDq8ikWAM",
    project_snapshot_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the Studio project.


**project_snapshot_id:** `str` — The ID of the Studio project snapshot.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.snapshots.stream(...)

#### 📝 Description

Stream the audio from a Studio project snapshot.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.snapshots.stream(
    project_id="project_id",
    project_snapshot_id="project_snapshot_id",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**project_snapshot_id:** `str` — The ID of the Studio project snapshot.


**convert_to_mpeg:** `typing.Optional[bool]` — Whether to convert the audio to mpeg format.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


client.studio.projects.snapshots.stream_archive(...)

#### 📝 Description

Returns a compressed archive of the Studio project's audio.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.snapshots.stream_archive(
    project_id="project_id",
    project_snapshot_id="project_snapshot_id",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**project_snapshot_id:** `str` — The ID of the Studio project snapshot.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## Studio Projects Chapters
client.studio.projects.chapters.list(...)

#### 📝 Description

Returns a list of a Studio project's chapters.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.list(
    project_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the Studio project.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.chapters.create(...)

#### 📝 Description

Creates a new chapter either as blank or from a URL.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.create(
    project_id="21m00Tcm4TlvDq8ikWAM",
    name="Chapter 1",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the Studio project.


**name:** `str` — The name of the chapter, used for identification only.


**from_url:** `typing.Optional[str]` — An optional URL from which we will extract content to initialize the Studio project. If this is set, 'from_url' and 'from_content' must be null. If neither 'from_url', 'from_document', 'from_content' are provided we will initialize the Studio project as blank.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.chapters.get(...)

#### 📝 Description

Returns information about a specific chapter.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.get(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.chapters.update(...)

#### 📝 Description

Updates a chapter.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.update(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.


**name:** `typing.Optional[str]` — The name of the chapter, used for identification only.


**content:** `typing.Optional[ChapterContentInputModel]` — The chapter content to use.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.chapters.delete(...)

#### 📝 Description

Deletes a chapter.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.delete(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.chapters.convert(...)

#### 📝 Description

Starts conversion of a specific chapter.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.convert(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Studio Projects Chapters Snapshots
client.studio.projects.chapters.snapshots.list(...)

#### 📝 Description

Gets information about all the snapshots of a chapter. Each snapshot can be downloaded as audio. Whenever a chapter is converted a snapshot will automatically be created.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.snapshots.list(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.chapters.snapshots.get(...)

#### 📝 Description

Returns the chapter snapshot.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.snapshots.get(
    project_id="21m00Tcm4TlvDq8ikWAM",
    chapter_id="21m00Tcm4TlvDq8ikWAM",
    chapter_snapshot_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the Studio project.


**chapter_id:** `str` — The ID of the chapter.


**chapter_snapshot_id:** `str` — The ID of the chapter snapshot.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.studio.projects.chapters.snapshots.stream(...)

#### 📝 Description

Stream the audio from a chapter snapshot. Use `GET /v1/studio/projects/{project_id}/chapters/{chapter_id}/snapshots` to return the snapshots of a chapter.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.studio.projects.chapters.snapshots.stream(
    project_id="project_id",
    chapter_id="chapter_id",
    chapter_snapshot_id="chapter_snapshot_id",
)

```

#### ⚙️ Parameters

**project_id:** `str` — The ID of the project to be used. You can use the [List projects](/docs/api-reference/studio/get-projects) endpoint to list all the available projects.


**chapter_id:** `str` — The ID of the chapter to be used. You can use the [List project chapters](/docs/api-reference/studio/get-chapters) endpoint to list all the available chapters.


**chapter_snapshot_id:** `str` — The ID of the chapter snapshot to be used. You can use the [List project chapter snapshots](/docs/api-reference/studio/get-snapshots) endpoint to list all the available snapshots.


**convert_to_mpeg:** `typing.Optional[bool]` — Whether to convert the audio to mpeg format.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## TextToVoice Preview
client.text_to_voice.preview.stream(...)

#### 📝 Description

Stream a voice preview that was created via the /v1/text-to-voice/design endpoint.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.text_to_voice.preview.stream(
    generated_voice_id="generated_voice_id",
)

```

#### ⚙️ Parameters

**generated_voice_id:** `str` — The generated_voice_id to stream.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## Tokens SingleUse
client.tokens.single_use.create()

#### 📝 Description

Generate a time limited single-use token with embedded authentication for frontend clients.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.tokens.single_use.create()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## User Subscription
client.user.subscription.get()

#### 📝 Description

Gets extended information about the users subscription

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.user.subscription.get()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Settings
client.voices.settings.get_default()

#### 📝 Description

Gets the default settings for voices. "similarity_boost" corresponds to"Clarity + Similarity Enhancement" in the web app and "stability" corresponds to "Stability" slider in the web app.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.settings.get_default()

```

#### ⚙️ Parameters

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.settings.get(...)

#### 📝 Description

Returns the settings for a specific voice. "similarity_boost" corresponds to"Clarity + Similarity Enhancement" in the web app and "stability" corresponds to "Stability" slider in the web app.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.settings.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.settings.update(...)

#### 📝 Description

Edit your settings for a specific voice. "similarity_boost" corresponds to "Clarity + Similarity Enhancement" in the web app and "stability" corresponds to "Stability" slider in the web app.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs, VoiceSettings

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.settings.update(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    request=VoiceSettings(
        stability=1.0,
        use_speaker_boost=True,
        similarity_boost=1.0,
        style=0.0,
        speed=1.0,
    ),
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**request:** `VoiceSettings`


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Ivc
client.voices.ivc.create(...)

#### 📝 Description

Create a voice clone and add it to your Voices

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.ivc.create(
    name="name",
)

```

#### ⚙️ Parameters

**name:** `str` — The name that identifies this voice. This will be displayed in the dropdown of the website.


**files:** `from __future__ import annotations

typing.List[core.File]` — See core.File for more documentation


**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.


**description:** `typing.Optional[str]` — A description of the voice.


**labels:** `typing.Optional[str]` — Serialized labels dictionary for the voice.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Pvc
client.voices.pvc.create(...)

#### 📝 Description

Creates a new PVC voice with metadata but no samples

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.create(
    name="John Smith",
    language="en",
)

```

#### ⚙️ Parameters

**name:** `str` — The name that identifies this voice. This will be displayed in the dropdown of the website.


**language:** `str` — Language used in the samples.


**description:** `typing.Optional[str]` — Description to use for the created voice.


**labels:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]` — Serialized labels dictionary for the voice.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.pvc.update(...)

#### 📝 Description

Edit PVC voice metadata

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.update(
    voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**name:** `typing.Optional[str]` — The name that identifies this voice. This will be displayed in the dropdown of the website.


**language:** `typing.Optional[str]` — Language used in the samples.


**description:** `typing.Optional[str]` — Description to use for the created voice.


**labels:** `typing.Optional[typing.Dict[str, typing.Optional[str]]]` — Serialized labels dictionary for the voice.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.pvc.train(...)

#### 📝 Description

Start PVC training process for a voice.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.train(
    voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**model_id:** `typing.Optional[str]` — The model ID to use for the conversion.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Pvc Samples
client.voices.pvc.samples.create(...)

#### 📝 Description

Add audio samples to a PVC voice

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.samples.create(
    voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**files:** `from __future__ import annotations

typing.List[core.File]` — See core.File for more documentation


**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.pvc.samples.update(...)

#### 📝 Description

Update a PVC voice sample - apply noise removal, select speaker, change trim times or file name.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.samples.update(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**sample_id:** `str` — Sample ID to be used


**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.


**selected_speaker_ids:** `typing.Optional[typing.Sequence[str]]` — Speaker IDs to be used for PVC training. Make sure you send all the speaker IDs you want to use for PVC training in one request because the last request will override the previous ones.


**trim_start_time:** `typing.Optional[int]` — The start time of the audio to be used for PVC training. Time should be in milliseconds


**trim_end_time:** `typing.Optional[int]` — The end time of the audio to be used for PVC training. Time should be in milliseconds


**file_name:** `typing.Optional[str]` — The name of the audio file to be used for PVC training.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.pvc.samples.delete(...)

#### 📝 Description

Delete a sample from a PVC voice.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.samples.delete(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**sample_id:** `str` — Sample ID to be used


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Pvc Verification
client.voices.pvc.verification.request(...)

#### 📝 Description

Request manual verification for a PVC voice.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.verification.request(
    voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**files:** `from __future__ import annotations

typing.List[core.File]` — See core.File for more documentation


**extra_text:** `typing.Optional[str]` — Extra text to be used in the manual verification process.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Pvc Samples Audio
client.voices.pvc.samples.audio.get(...)

#### 📝 Description

Retrieve the first 30 seconds of voice sample audio with or without noise removal.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.samples.audio.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
    remove_background_noise=True,
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**sample_id:** `str` — Sample ID to be used


**remove_background_noise:** `typing.Optional[bool]` — If set will remove background noise for voice samples using our audio isolation model. If the samples do not include background noise, it can make the quality worse.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Pvc Samples Waveform
client.voices.pvc.samples.waveform.get(...)

#### 📝 Description

Retrieve the visual waveform of a voice sample.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.samples.waveform.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**sample_id:** `str` — Sample ID to be used


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Pvc Samples Speakers
client.voices.pvc.samples.speakers.get(...)

#### 📝 Description

Retrieve the status of the speaker separation process and the list of detected speakers if complete.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.samples.speakers.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**sample_id:** `str` — Sample ID to be used


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.pvc.samples.speakers.separate(...)

#### 📝 Description

Start speaker separation process for a sample

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.samples.speakers.separate(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**sample_id:** `str` — Sample ID to be used


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Pvc Samples Speakers Audio
client.voices.pvc.samples.speakers.audio.get(...)

#### 📝 Description

Retrieve the separated audio for a specific speaker.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.samples.speakers.audio.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    sample_id="VW7YKqPnjY4h39yTbx2L",
    speaker_id="VW7YKqPnjY4h39yTbx2L",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**sample_id:** `str` — Sample ID to be used


**speaker_id:** `str` — Speaker ID to be used, you can use GET https://api.elevenlabs.io/v1/voices/{voice_id}/samples/{sample_id}/speakers to list all the available speakers for a sample.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Pvc Verification Captcha
client.voices.pvc.verification.captcha.get(...)

#### 📝 Description

Get captcha for PVC voice verification.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.verification.captcha.get(
    voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.voices.pvc.verification.captcha.verify(...)

#### 📝 Description

Submit captcha verification for PVC voice.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.pvc.verification.captcha.verify(
    voice_id="21m00Tcm4TlvDq8ikWAM",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — Voice ID to be used, you can use https://api.elevenlabs.io/v1/voices to list all the available voices.


**recording:** `from __future__ import annotations

core.File` — See core.File for more documentation


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Voices Samples Audio
client.voices.samples.audio.get(...)

#### 📝 Description

Returns the audio corresponding to a sample attached to a voice.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.voices.samples.audio.get(
    voice_id="voice_id",
    sample_id="sample_id",
)

```

#### ⚙️ Parameters

**voice_id:** `str` — ID of the voice to be used. You can use the [Get voices](/docs/api-reference/voices/search) endpoint list all the available voices.


**sample_id:** `str` — ID of the sample to be used. You can use the [Get voices](/docs/api-reference/voices/get) endpoint list all the available samples for a voice.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.


## Workspace Groups
client.workspace.groups.search(...)

#### 📝 Description

Searches for user groups in the workspace. Multiple or no groups may be returned.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.groups.search(
    name="name",
)

```

#### ⚙️ Parameters

**name:** `str` — Name of the target group.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Workspace Invites
client.workspace.invites.create(...)

#### 📝 Description

Sends an email invitation to join your workspace to the provided email. If the user doesn't have an account they will be prompted to create one. If the user accepts this invite they will be added as a user to your workspace and your subscription using one of your seats. This endpoint may only be called by workspace administrators. If the user is already in the workspace a 400 error will be returned.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.invites.create(
    email="john.doe@testmail.com",
)

```

#### ⚙️ Parameters

**email:** `str` — The email of the customer


**group_ids:** `typing.Optional[typing.Sequence[str]]` — The group ids of the user


**workspace_permission:** `typing.Optional[BodyInviteUserV1WorkspaceInvitesAddPostWorkspacePermission]` — The workspace permission of the user


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.workspace.invites.create_batch(...)

#### 📝 Description

Sends email invitations to join your workspace to the provided emails. Requires all email addresses to be part of a verified domain. If the users don't have an account they will be prompted to create one. If the users accept these invites they will be added as users to your workspace and your subscription using one of your seats. This endpoint may only be called by workspace administrators.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.invites.create_batch(
    emails=["emails"],
)

```

#### ⚙️ Parameters

**emails:** `typing.Sequence[str]` — The email of the customer


**group_ids:** `typing.Optional[typing.Sequence[str]]` — The group ids of the user


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.workspace.invites.delete(...)

#### 📝 Description

Invalidates an existing email invitation. The invitation will still show up in the inbox it has been delivered to, but activating it to join the workspace won't work. This endpoint may only be called by workspace administrators.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.invites.delete(
    email="john.doe@testmail.com",
)

```

#### ⚙️ Parameters

**email:** `str` — The email of the customer


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Workspace Members
client.workspace.members.update(...)

#### 📝 Description

Updates attributes of a workspace member. Apart from the email identifier, all parameters will remain unchanged unless specified. This endpoint may only be called by workspace administrators.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.members.update(
    email="email",
)

```

#### ⚙️ Parameters

**email:** `str` — Email of the target user.


**is_locked:** `typing.Optional[bool]` — Whether to lock or unlock the user account.


**workspace_role:** `typing.Optional[BodyUpdateMemberV1WorkspaceMembersPostWorkspaceRole]` — Role dictating permissions in the workspace.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Workspace Resources
client.workspace.resources.get(...)

#### 📝 Description

Gets the metadata of a resource by ID.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.resources.get(
    resource_id="resource_id",
    resource_type="voice",
)

```

#### ⚙️ Parameters

**resource_id:** `str` — The ID of the target resource.


**resource_type:** `WorkspaceResourceType` — Resource type of the target resource.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.workspace.resources.share(...)

#### 📝 Description

Grants a role on a workspace resource to a user or a group. It overrides any existing role this user/service account/group/workspace api key has on the resource. To target a user or service account, pass only the user email. The user must be in your workspace. To target a group, pass only the group id. To target a workspace api key, pass the api key id. The resource will be shared with the service account associated with the api key. You must have admin access to the resource to share it.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.resources.share(
    resource_id="resource_id",
    role="admin",
    resource_type="voice",
)

```

#### ⚙️ Parameters

**resource_id:** `str` — The ID of the target resource.


**role:** `BodyShareWorkspaceResourceV1WorkspaceResourcesResourceIdSharePostRole` — Role to update the target principal with.


**resource_type:** `WorkspaceResourceType` — Resource type of the target resource.


**user_email:** `typing.Optional[str]` — The email of the user or service account.


**group_id:** `typing.Optional[str]` — The ID of the target group. To target the permissions principals have by default on this resource, use the value 'default'.


**workspace_api_key_id:** `typing.Optional[str]` — The ID of the target workspace API key. This isn't the same as the key itself that would you pass in the header for authentication. Workspace admins can find this in the workspace settings UI.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.workspace.resources.unshare(...)

#### 📝 Description

Removes any existing role on a workspace resource from a user, service account, group or workspace api key. To target a user or service account, pass only the user email. The user must be in your workspace. To target a group, pass only the group id. To target a workspace api key, pass the api key id. The resource will be unshared from the service account associated with the api key. You must have admin access to the resource to unshare it. You cannot remove permissions from the user who created the resource.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.resources.unshare(
    resource_id="resource_id",
    resource_type="voice",
)

```

#### ⚙️ Parameters

**resource_id:** `str` — The ID of the target resource.


**resource_type:** `WorkspaceResourceType` — Resource type of the target resource.


**user_email:** `typing.Optional[str]` — The email of the user or service account.


**group_id:** `typing.Optional[str]` — The ID of the target group. To target the permissions principals have by default on this resource, use the value 'default'.


**workspace_api_key_id:** `typing.Optional[str]` — The ID of the target workspace API key. This isn't the same as the key itself that would you pass in the header for authentication. Workspace admins can find this in the workspace settings UI.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


## Workspace Groups Members
client.workspace.groups.members.remove(...)

#### 📝 Description

Removes a member from the specified group. This endpoint may only be called by workspace administrators.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.groups.members.remove(
    group_id="group_id",
    email="email",
)

```

#### ⚙️ Parameters

**group_id:** `str` — The ID of the target group.


**email:** `str` — The email of the target workspace member.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


client.workspace.groups.members.add(...)

#### 📝 Description

Adds a member of your workspace to the specified group. This endpoint may only be called by workspace administrators.

#### 🔌 Usage

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(
    api_key="YOUR_API_KEY",
)
client.workspace.groups.members.add(
    group_id="group_id",
    email="email",
)

```

#### ⚙️ Parameters

**group_id:** `str` — The ID of the target group.


**email:** `str` — The email of the target workspace member.


**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.


