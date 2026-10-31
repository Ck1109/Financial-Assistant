# Local architecture

The first demonstrable slice is a modular localhost application. Source bytes are
preserved by content hash, extracted pages become citeable context segments, a
replaceable retrieval adapter selects evidence, and a replaceable language-model
adapter summarizes only that evidence.

The default adapters are deterministic and local so learners can run the workflow
without credentials. Provider factories fail explicitly for unsupported names.
Future model and vector-store adapters must preserve the same ports and answer
contract.

## Data handling

Raw source bytes and extracted artifacts belong under the local `data/` directory.
They are excluded from source control by default. Logs must use run identifiers and
must redact credential-shaped values. Do not place private financial information in
fixtures or committed configuration.

## Safety boundary

An answered claim requires a citation. Missing evidence produces an explicit
insufficiency result. Personalized buy, sell, or hold recommendations are rejected.
The UI describes observable workflow stages rather than private chain-of-thought.

