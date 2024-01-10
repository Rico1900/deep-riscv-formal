from parsy import string, regex, seq, digit, letter
from datetime import timedelta
from dataclasses import dataclass

@dataclass
class EnginePerformance:
    name: str
    time_consumption: int

    def __str__(self):
        return f"engine_name={self.name}, time_consumption={self.time_consumption}"


whitespace = regex(r"\s*")


def lexeme(p):
    return p << whitespace


letter_or_dash = string('_') | letter | digit

time_stamp = (regex(r'[0-9]{1,2}').map(int)
              .sep_by(string(":"), min=3, max=3)
              .combine(lambda h, m, s: timedelta(hours=h, minutes=m, seconds=s)))

engine_name = (seq(string('['), letter_or_dash.many(), string(']'))
               .map(lambda seqs: ''.join(seqs[1])))

time_consumption = (seq(string('('), digit.many(), string(')'))
                    .map(lambda seqs: int(''.join(seqs[1]))))

clock_time_summary = seq(
    lexeme(string('SBY')),
    lexeme(time_stamp),
    lexeme(engine_name),
    lexeme(string('summary: Elapsed clock time [H:MM:SS (secs)]:')),
    lexeme(time_stamp),
    lexeme(time_consumption)
).map(lambda seqs: EnginePerformance(name=seqs[2], time_consumption=seqs[5]))

if __name__ == '__main__':
    print(clock_time_summary.parse("SBY 15:17:55 [pc_bwd_ch0_abc_bmc3] summary: Elapsed clock time [H:MM:SS (secs)]: 0:01:07 (67)"))
