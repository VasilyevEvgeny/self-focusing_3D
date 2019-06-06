from abc import ABCMeta, abstractmethod
from PIL import Image


from core import parse_args, create_dir, create_multidir, make_animation, make_video


class BaseMultimedia(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        self._args = parse_args()
        self._results_dir, self._results_dir_name = create_multidir(self._args.global_root_dir,
                                                                    self._args.global_results_dir_name,
                                                                    self._args.prefix)

    @abstractmethod
    def _get_data(self, plot_beam_func):
        """get_data"""

    @abstractmethod
    def process_multimedia(self):
        """process_multimedia"""

    def _compose(self, all_files, indices, n_pictures_max, fps=10, animation=True, video=True):
        all_files_upd = []
        for idx in range(len(all_files)):
            files = []
            for file in all_files[idx]:
                files.append(file)

            # append last picture if n_pictures < n_pictures_max
            delta = n_pictures_max - len(files)
            for i in range(delta):
                files.append(all_files[idx][-1])

            # 1 second pause at the beginning
            for i in range(fps):
                files = [all_files[idx][0]] + files

            # 1 second pause at the end
            for i in range(fps):
                files.append(all_files[idx][-1])

            all_files_upd.append(files)

        # save composed images to dir
        results_dir = create_dir(path=self._results_dir)
        width, height = Image.open(all_files_upd[0][0]).size
        i1_max, i2_max = indices[-1]
        total_width, total_height = (i1_max + 1) * width, (i2_max + 1) * height
        for i in range(len(all_files_upd[0])):
            composed_im = Image.new('RGB', (total_width, total_height))
            for j in range(len(all_files_upd)):
                im = Image.open(all_files_upd[j][i])
                i1, i2 = indices[j]
                composed_im.paste(im, (i1 * width, i2 * height))
            composed_im.save(results_dir + '/%04d.png' % i, 'PNG')

        if animation:
            make_animation(root_dir=self._results_dir,
                           name=self._args.prefix,
                           fps=fps)

        if video:
            make_video(root_dir=self._results_dir,
                       name=self._args.prefix,
                       fps=fps)
