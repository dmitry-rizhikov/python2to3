import difflib
import logging


class Diff:
    logger = logging.getLogger(__name__)

    def diff_files(self, from_file, to_file, out_file='pylint2_diff.txt'):
        with open(from_file, 'r') as old:
            with open(to_file, 'r') as new:
                diff = difflib.unified_diff(
                    old.readlines(),
                    new.readlines(),
                    fromfile='old',
                    tofile='new',
                )

                self.logger.info('diff %s and %s', from_file, to_file)

        file = open(out_file, 'w')

        for line in diff:
            file.write(line)
            # if line.startswith('+'):
            #     file.write(line)

        file.close()
